#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
RUNTIME_DIR = ROOT / ".runtime"
LOG_DIR = RUNTIME_DIR / "logs"
BASE_PYTHON_MARKER = VENV_DIR / ".sonicforge_base_python"
DEFAULT_LOCAL_LLM_MODEL = os.getenv("SATYA_ACADEMY_LLM_MODEL", "qwen2.5:3b").strip() or "qwen2.5:3b"
LLAMA_CPP_PORT = int(os.getenv("SATYA_ACADEMY_LLAMA_CPP_PORT", "8012"))
LLAMA_CPP_BACKEND_PORT = int(os.getenv("SATYA_ACADEMY_LLAMA_CPP_BACKEND_PORT", "8013"))
LLAMA_CPP_ENDPOINT = f"http://127.0.0.1:{LLAMA_CPP_PORT}/v1"
DEFAULT_LLAMA_CPP_HF_REPO = os.getenv(
    "SATYA_ACADEMY_LLAMA_CPP_REPO",
    "Qwen/Qwen2.5-1.5B-Instruct-GGUF",
).strip() or "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
DEFAULT_LLAMA_CPP_HF_FILE = os.getenv(
    "SATYA_ACADEMY_LLAMA_CPP_FILE",
    "qwen2.5-1.5b-instruct-q4_k_m.gguf",
).strip() or "qwen2.5-1.5b-instruct-q4_k_m.gguf"


class RunnerError(RuntimeError):
    pass


@dataclass
class PythonProbe:
    executable: str
    version: tuple[int, int, int]
    has_tk: bool


def info(message: str) -> None:
    print(f"[SonicForge] {message}", flush=True)


def warn(message: str) -> None:
    print(f"[SonicForge][warn] {message}", flush=True)


def fail(message: str) -> None:
    raise RunnerError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Master runner for SNSAI SonicForge X.",
    )
    parser.add_argument(
        "--mode",
        choices=("web", "desktop", "both"),
        default="web",
        help="Runtime mode to launch.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the web server.",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip compile and unittest validation before launch.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run environment checks and validation only, then exit.",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Kill stale SonicForge processes and exit.",
    )
    parser.add_argument(
        "--open-browser",
        action="store_true",
        help="Open the web UI after the server becomes healthy.",
    )
    parser.add_argument(
        "--setup-llm",
        action="store_true",
        help="Install, prepare, and keep the local llama.cpp language model server running for the academy assistant.",
    )
    return parser.parse_args()


def candidate_pythons() -> list[str]:
    candidates = [
        sys.executable,
        shutil.which("python3"),
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
        "/opt/homebrew/bin/python3.14",
        "/opt/homebrew/bin/python3.11",
        "/usr/local/bin/python3",
        "/usr/bin/python3",
    ]
    unique: list[str] = []
    for item in candidates:
        if not item:
            continue
        path_obj = Path(item)
        try:
            resolved = path_obj.resolve()
        except FileNotFoundError:
            continue
        if VENV_DIR in resolved.parents:
            continue
        path = str(resolved)
        if path not in unique and resolved.exists():
            unique.append(path)
    return unique


def probe_python(python_executable: str) -> PythonProbe | None:
    cmd = [
        python_executable,
        "-c",
        (
            "import json, sys\n"
            "probe = {'executable': sys.executable, 'version': list(sys.version_info[:3])}\n"
            "try:\n"
            "    import tkinter\n"
            "    probe['has_tk'] = True\n"
            "except Exception:\n"
            "    probe['has_tk'] = False\n"
            "print(json.dumps(probe))"
        ),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        return None
    version = tuple(payload["version"])
    return PythonProbe(
        executable=payload["executable"],
        version=(int(version[0]), int(version[1]), int(version[2])),
        has_tk=bool(payload["has_tk"]),
    )


def choose_base_python(mode: str) -> PythonProbe:
    probes = [probe for candidate in candidate_pythons() if (probe := probe_python(candidate))]
    if not probes:
        fail("No working Python 3 interpreter was found.")

    supported = [probe for probe in probes if probe.version >= (3, 11, 0)]
    if not supported:
        fail("Python 3.11+ is required, but no compatible interpreter was found.")

    require_tk = mode in {"desktop", "both"}
    if require_tk:
        tk_capable = [probe for probe in supported if probe.has_tk]
        if not tk_capable:
            lines = ["Desktop mode needs a Tk-capable Python interpreter. Probed:"]
            lines.extend(
                f"- {probe.executable}  version {'.'.join(map(str, probe.version))}  tkinter={probe.has_tk}"
                for probe in supported
            )
            fail("\n".join(lines))
        return sorted(tk_capable, key=lambda probe: probe.version, reverse=True)[0]
    return sorted(supported, key=lambda probe: probe.version, reverse=True)[0]


def run_command(
    cmd: list[str],
    *,
    check: bool = True,
    capture_output: bool = False,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=capture_output,
        env=env,
    )
    if check and result.returncode != 0:
        if capture_output:
            raise RunnerError(
                f"Command failed: {' '.join(cmd)}\n{result.stdout}\n{result.stderr}".strip()
            )
        raise RunnerError(f"Command failed: {' '.join(cmd)}")
    return result


def ensure_runtime_dirs() -> None:
    RUNTIME_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def ensure_venv(base_python: PythonProbe) -> Path:
    needs_rebuild = True
    venv_python = VENV_DIR / "bin" / "python"
    if venv_python.exists():
        probe = probe_python(str(venv_python))
        active_venv = Path(os.getenv("VIRTUAL_ENV", "")).resolve() if os.getenv("VIRTUAL_ENV") else None
        using_target_venv = active_venv == VENV_DIR.resolve() if active_venv else False
        if probe and probe.version >= (3, 11, 0) and (base_python.has_tk <= probe.has_tk or not base_python.has_tk):
            previous = BASE_PYTHON_MARKER.read_text().strip() if BASE_PYTHON_MARKER.exists() else ""
            if using_target_venv or previous in {"", base_python.executable, probe.executable}:
                needs_rebuild = False
                BASE_PYTHON_MARKER.write_text(probe.executable)

    if needs_rebuild:
        if VENV_DIR.exists():
            info("Rebuilding virtual environment to match the selected Python runtime...")
            shutil.rmtree(VENV_DIR)
        else:
            info("Creating virtual environment...")
        run_command([base_python.executable, "-m", "venv", str(VENV_DIR)])
        BASE_PYTHON_MARKER.write_text(base_python.executable)

    venv_python = VENV_DIR / "bin" / "python"
    if not venv_python.exists():
        fail("Virtual environment creation failed: missing .venv/bin/python")

    maybe_install_requirements(venv_python)
    return venv_python


def maybe_install_requirements(venv_python: Path) -> None:
    requirements_files = [
        ROOT / "requirements.txt",
        ROOT / "requirements-dev.txt",
    ]
    files_to_install = [
        path for path in requirements_files if path.exists() and path.read_text().strip()
    ]
    if not files_to_install:
        info("No external Python requirements declared; skipping pip install.")
        return

    info("Installing Python requirements...")
    run_command([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
    for requirements in files_to_install:
        run_command([str(venv_python), "-m", "pip", "install", "-r", str(requirements)])


def find_llama_server() -> str | None:
    candidates = [
        shutil.which("llama-server"),
        "/opt/homebrew/bin/llama-server",
        "/usr/local/bin/llama-server",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(Path(candidate))
    return None


def install_llama_cpp() -> str:
    server = find_llama_server()
    if server:
        info(f"Found llama.cpp server at {server}")
        return server

    brew = shutil.which("brew")
    if not brew:
        fail("Homebrew is required to install llama.cpp automatically, but brew was not found.")

    info("Installing llama.cpp through Homebrew...")
    run_command([brew, "install", "llama.cpp"])
    server = find_llama_server()
    if not server:
        fail("llama.cpp installed, but llama-server was not found on the machine.")
    return server


def wait_for_llm(url: str, timeout_seconds: float = 30.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(1.0)
            continue
    fail(f"Local LLM health check failed for {url}")


def start_llama_cpp_server() -> tuple[subprocess.Popen[str], Path]:
    server_path = install_llama_cpp()
    log_path = LOG_DIR / "llm.log"
    backend_log_path = LOG_DIR / "llm-backend.log"
    env = os.environ.copy()
    env["SATYA_ACADEMY_LLAMA_SERVER_BIN"] = server_path
    env["SATYA_ACADEMY_LLAMA_CPP_PORT"] = str(LLAMA_CPP_PORT)
    env["SATYA_ACADEMY_LLAMA_CPP_BACKEND_PORT"] = str(LLAMA_CPP_BACKEND_PORT)
    env["SATYA_ACADEMY_LLAMA_CPP_REPO"] = DEFAULT_LLAMA_CPP_HF_REPO
    env["SATYA_ACADEMY_LLAMA_CPP_FILE"] = DEFAULT_LLAMA_CPP_HF_FILE
    env["SATYA_ACADEMY_LLAMA_CPP_LOG"] = str(backend_log_path)
    cmd = [
        str(VENV_DIR / "bin" / "python"),
        "-m",
        "sonicforge.apps.llm_gateway",
    ]
    info(
        f"Starting local academy LLM gateway on {LLAMA_CPP_ENDPOINT} "
        f"using {DEFAULT_LLAMA_CPP_HF_REPO} / {DEFAULT_LLAMA_CPP_HF_FILE}"
    )
    process = launch_process(cmd, log_path, env=env)
    try:
        wait_for_llm(LLAMA_CPP_ENDPOINT)
    except RunnerError:
        terminate_process(process)
        raise RunnerError(
            "Local academy LLM gateway did not become healthy.\n"
            f"Recent gateway log:\n{read_log_tail(log_path)}\n\nRecent backend log:\n{read_log_tail(backend_log_path)}"
        )
    return process, log_path


def discover_stale_pids(port: int) -> set[int]:
    pids: set[int] = set()
    current_pid = os.getpid()

    for pattern in ("sonicforge.apps.server", "sonicforge.apps.desktop", "run_sonicforge.py"):
        result = subprocess.run(
            ["pgrep", "-f", pattern],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.strip().isdigit():
                    pid = int(line.strip())
                    if pid != current_pid:
                        pids.add(pid)

    result = subprocess.run(
        ["lsof", "-ti", f"tcp:{port}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            if line.strip().isdigit():
                pid = int(line.strip())
                if pid != current_pid:
                    pids.add(pid)

    return pids


def terminate_pids(pids: Iterable[int]) -> None:
    pid_list = sorted(set(pids))
    if not pid_list:
        info("No stale SonicForge processes found.")
        return

    info(f"Stopping stale SonicForge processes: {', '.join(map(str, pid_list))}")
    for pid in pid_list:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            continue

    time.sleep(1.0)
    for pid in pid_list:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            continue
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            continue


def run_validation(venv_python: Path) -> None:
    info("Running compile checks...")
    run_command([str(venv_python), "-m", "compileall", "sonicforge", "tests"])
    info("Running unit tests...")
    run_command([str(venv_python), "-m", "unittest", "discover", "-s", "tests"])
    info("Running import smoke tests...")
    smoke = (
        "from sonicforge.core.session import create_project\n"
        "project = create_project('Smoke', 'cinematic-electronic', 118, 8, 60, 68, 48)\n"
        "print(project.name, len(project.tracks), project.key, project.mode)"
    )
    run_command([str(venv_python), "-c", smoke])


def launch_process(cmd: list[str], log_path: Path, env: dict[str, str] | None = None) -> subprocess.Popen[str]:
    log_file = log_path.open("w", encoding="utf-8")
    process = subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
        env=env,
    )
    return process


def wait_for_http(url: str, timeout_seconds: float = 20.0) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.5)
            continue
    fail(f"Web health check failed for {url}")


def read_log_tail(path: Path, max_lines: int = 60) -> str:
    if not path.exists():
        return "(log file not created)"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-max_lines:])


def start_web(venv_python: Path, port: int) -> tuple[subprocess.Popen[str], Path]:
    log_path = LOG_DIR / "web.log"
    env = os.environ.copy()
    env["SATYA_ACADEMY_LLAMA_CPP_ENDPOINT"] = LLAMA_CPP_ENDPOINT
    cmd = [
        str(venv_python),
        "-c",
        f"from sonicforge.apps.server import run_server; run_server(port={port})",
    ]
    info(f"Starting web server on http://127.0.0.1:{port}")
    process = launch_process(cmd, log_path, env=env)
    try:
        wait_for_http(f"http://127.0.0.1:{port}/api/health")
    except RunnerError:
        terminate_process(process)
        info("Retrying web server once after cleanup...")
        terminate_pids(discover_stale_pids(port))
        process = launch_process(cmd, log_path, env=env)
        wait_for_http(f"http://127.0.0.1:{port}/api/health")
    return process, log_path


def start_desktop(venv_python: Path) -> tuple[subprocess.Popen[str], Path]:
    log_path = LOG_DIR / "desktop.log"
    cmd = [str(venv_python), "-m", "sonicforge.apps.desktop"]
    info("Starting desktop application...")
    process = launch_process(cmd, log_path)
    time.sleep(2.0)
    if process.poll() is not None:
        raise RunnerError(
            "Desktop app exited during startup.\n"
            f"Recent desktop log:\n{read_log_tail(log_path)}"
        )
    return process, log_path


def open_browser(url: str) -> None:
    opener = shutil.which("open") or shutil.which("xdg-open")
    if not opener:
        warn(f"Browser opener not found. Open {url} manually.")
        return
    subprocess.Popen([opener, url], cwd=ROOT)


def terminate_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    try:
        process.terminate()
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
    except ProcessLookupError:
        return


def monitor(mode: str, web_process: subprocess.Popen[str] | None, desktop_process: subprocess.Popen[str] | None, port: int) -> None:
    info("System is running. Press Ctrl+C to stop everything cleanly.")
    if mode == "web" and web_process:
        return_code = web_process.wait()
        if return_code != 0:
            raise RunnerError(
                f"Web server exited unexpectedly with code {return_code}.\n"
                f"Recent log:\n{read_log_tail(LOG_DIR / 'web.log')}"
            )
        return

    if mode == "desktop" and desktop_process:
        return_code = desktop_process.wait()
        if return_code != 0:
            raise RunnerError(
                f"Desktop app exited unexpectedly with code {return_code}.\n"
                f"Recent log:\n{read_log_tail(LOG_DIR / 'desktop.log')}"
            )
        return

    assert web_process is not None and desktop_process is not None
    while True:
        web_code = web_process.poll()
        desktop_code = desktop_process.poll()
        if web_code is not None:
            raise RunnerError(
                f"Web server exited unexpectedly with code {web_code}.\n"
                f"Recent web log:\n{read_log_tail(LOG_DIR / 'web.log')}"
            )
        if desktop_code is not None:
            if desktop_code != 0:
                raise RunnerError(
                    f"Desktop app exited unexpectedly with code {desktop_code}.\n"
                    f"Recent desktop log:\n{read_log_tail(LOG_DIR / 'desktop.log')}"
                )
            info("Desktop app closed. Shutting down web server.")
            return
        try:
            wait_for_http(f"http://127.0.0.1:{port}/api/health", timeout_seconds=2.5)
        except RunnerError:
            raise RunnerError(
                "Web server health check failed during runtime.\n"
                f"Recent web log:\n{read_log_tail(LOG_DIR / 'web.log')}"
            )
        time.sleep(2.0)


def monitor_llm(llm_process: subprocess.Popen[str] | None) -> None:
    if llm_process is None:
        fail("Local academy LLM process did not start.")

    info(f"Local academy LLM is running at {LLAMA_CPP_ENDPOINT}. Press Ctrl+C to stop it cleanly.")
    return_code = llm_process.wait()
    if return_code != 0:
        raise RunnerError(
            f"Local academy LLM exited unexpectedly with code {return_code}.\n"
            f"Recent LLM log:\n{read_log_tail(LOG_DIR / 'llm.log')}"
        )


def main() -> int:
    args = parse_args()
    ensure_runtime_dirs()
    info(f"Workspace: {ROOT}")

    base_python = choose_base_python(args.mode)
    info(
        "Selected base Python: "
        f"{base_python.executable} "
        f"(version {'.'.join(map(str, base_python.version))}, tkinter={base_python.has_tk})"
    )
    venv_python = ensure_venv(base_python)
    info(f"Using virtual environment interpreter: {venv_python}")

    terminate_pids(discover_stale_pids(args.port))
    terminate_pids(discover_stale_pids(LLAMA_CPP_PORT))
    terminate_pids(discover_stale_pids(LLAMA_CPP_BACKEND_PORT))
    if args.clean_only:
        info("Cleanup completed.")
        return 0

    if not args.skip_tests:
        run_validation(venv_python)
    else:
        warn("Skipping validation checks by request.")

    if args.check_only:
        info("Check-only run completed successfully.")
        return 0

    web_process: subprocess.Popen[str] | None = None
    desktop_process: subprocess.Popen[str] | None = None
    llm_process: subprocess.Popen[str] | None = None

    try:
        if args.setup_llm:
            llm_process, _ = start_llama_cpp_server()
            info(f"Local academy LLM is healthy at {LLAMA_CPP_ENDPOINT}")
            info("LLM setup completed successfully.")
            monitor_llm(llm_process)
            return 0

        if args.mode in {"web", "both"} and find_llama_server():
            try:
                llm_process, _ = start_llama_cpp_server()
                info(f"Local academy LLM is running at {LLAMA_CPP_ENDPOINT}")
            except RunnerError as exc:
                warn(str(exc))
                llm_process = None

        if args.mode in {"web", "both"}:
            web_process, _ = start_web(venv_python, args.port)
            info(f"Web UI healthy at http://127.0.0.1:{args.port}")
            if args.open_browser:
                open_browser(f"http://127.0.0.1:{args.port}")

        if args.mode in {"desktop", "both"}:
            desktop_process, _ = start_desktop(venv_python)
            info("Desktop application started.")

        monitor(args.mode, web_process, desktop_process, args.port)
        return 0
    except KeyboardInterrupt:
        info("Shutdown requested. Stopping SonicForge services...")
        return 130
    finally:
        terminate_process(desktop_process)
        terminate_process(web_process)
        terminate_process(llm_process)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RunnerError as exc:
        print(f"[SonicForge][error] {exc}", file=sys.stderr)
        raise SystemExit(1)
