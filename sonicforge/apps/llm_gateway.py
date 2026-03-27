from __future__ import annotations

import json
import os
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


GATEWAY_HOST = os.getenv("SATYA_ACADEMY_LLAMA_CPP_HOST", "127.0.0.1").strip() or "127.0.0.1"
GATEWAY_PORT = int(os.getenv("SATYA_ACADEMY_LLAMA_CPP_PORT", "8012"))
BACKEND_PORT = int(os.getenv("SATYA_ACADEMY_LLAMA_CPP_BACKEND_PORT", "8013"))
HF_REPO = os.getenv("SATYA_ACADEMY_LLAMA_CPP_REPO", "Qwen/Qwen2.5-1.5B-Instruct-GGUF").strip() or "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
HF_FILE = os.getenv("SATYA_ACADEMY_LLAMA_CPP_FILE", "qwen2.5-1.5b-instruct-q4_k_m.gguf").strip() or "qwen2.5-1.5b-instruct-q4_k_m.gguf"
LLAMA_SERVER_BIN = os.getenv("SATYA_ACADEMY_LLAMA_SERVER_BIN", shutil.which("llama-server") or "/opt/homebrew/bin/llama-server").strip()
LLAMA_CONTEXT = int(os.getenv("SATYA_ACADEMY_LLAMA_CPP_CONTEXT", "4096"))
LLAMA_NGL = os.getenv("SATYA_ACADEMY_LLAMA_CPP_NGL", "99").strip() or "99"
MAX_JSON_BODY_BYTES = 8 * 1024 * 1024
LOG_PATH = Path(os.getenv("SATYA_ACADEMY_LLAMA_CPP_LOG", str(Path(__file__).resolve().parents[2] / ".runtime" / "logs" / "llm-backend.log")))


def fetch_json(url: str, timeout: float = 1.5, method: str = "GET", data: dict | None = None) -> dict:
    headers = {"User-Agent": "SatyaSangeetLLMGateway/1.0"}
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, headers=headers, data=body, method=method)
    with urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def model_cache_dir() -> Path:
    repo_dir = HF_REPO.replace("/", "--")
    return Path.home() / ".cache" / "huggingface" / "hub" / f"models--{repo_dir}"


def bytes_to_human(size: int) -> str:
    value = float(max(size, 0))
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


@dataclass
class BackendState:
    state: str
    ready: bool
    model_id: str
    detail: str
    endpoint: str
    download_bytes: int = 0

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "ready": self.ready,
            "model": self.model_id,
            "detail": self.detail,
            "endpoint": self.endpoint,
            "download_bytes": self.download_bytes,
            "download_human": bytes_to_human(self.download_bytes),
        }


class LLMBackendManager:
    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.lock = threading.Lock()
        self.last_error = ""
        self.start_requested = False

    @property
    def backend_url(self) -> str:
        return f"http://127.0.0.1:{BACKEND_PORT}/v1"

    def download_progress_bytes(self) -> int:
        cache_dir = model_cache_dir()
        if not cache_dir.exists():
            return 0
        largest = 0
        for path in cache_dir.rglob("*.downloadInProgress"):
            try:
                largest = max(largest, path.stat().st_size)
            except OSError:
                continue
        return largest

    def is_ready(self) -> bool:
        try:
            payload = fetch_json(f"{self.backend_url}/models", timeout=0.8)
        except (TimeoutError, URLError, json.JSONDecodeError, ValueError):
            return False
        models = payload.get("data", []) if isinstance(payload, dict) else []
        return bool(models)

    def ensure_started(self) -> None:
        with self.lock:
            if self.process and self.process.poll() is None:
                return
            self.start_requested = True
            self.last_error = ""
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            log_file = LOG_PATH.open("w", encoding="utf-8")
            cmd = [
                LLAMA_SERVER_BIN,
                "--hf-repo",
                HF_REPO,
                "--hf-file",
                HF_FILE,
                "--host",
                "127.0.0.1",
                "--port",
                str(BACKEND_PORT),
                "-ngl",
                LLAMA_NGL,
                "-c",
                str(LLAMA_CONTEXT),
            ]
            self.process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
            )

    def status(self) -> BackendState:
        self.ensure_started()

        if self.is_ready():
            return BackendState(
                state="ready",
                ready=True,
                model_id=f"{HF_REPO}:{HF_FILE}",
                detail="The local academy model is fully loaded and ready for chat completions.",
                endpoint=f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/v1",
            )

        if self.process and self.process.poll() is not None:
            self.last_error = f"llama.cpp backend exited with code {self.process.returncode}."
            return BackendState(
                state="error",
                ready=False,
                model_id=f"{HF_REPO}:{HF_FILE}",
                detail=self.last_error,
                endpoint=f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/v1",
                download_bytes=self.download_progress_bytes(),
            )

        progress = self.download_progress_bytes()
        detail = "The local academy model is starting."
        if progress > 0:
            detail = f"The local academy model is downloading and warming up. Current downloaded size: {bytes_to_human(progress)}."
        return BackendState(
            state="loading",
            ready=False,
            model_id=f"{HF_REPO}:{HF_FILE}",
            detail=detail,
            endpoint=f"http://{GATEWAY_HOST}:{GATEWAY_PORT}/v1",
            download_bytes=progress,
        )

    def proxy_chat(self, payload: dict) -> tuple[int, bytes, str]:
        request = Request(
            f"{self.backend_url}/chat/completions",
            headers={"Content-Type": "application/json", "User-Agent": "SatyaSangeetLLMGateway/1.0"},
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "application/json; charset=utf-8")
            return response.status, body, content_type

    def stop(self) -> None:
        with self.lock:
            if not self.process or self.process.poll() is not None:
                return
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


MANAGER = LLMBackendManager()


class GatewayServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "SatyaSangeetLLMGateway/0.1"

    def log_message(self, fmt: str, *args) -> None:
        return None

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        status = MANAGER.status()
        if path in {"/", "/v1", "/health", "/v1/health"}:
            return self._json_response(status.to_dict())
        if path == "/v1/models":
            payload = {
                "object": "list",
                "data": [],
                "ready": status.ready,
                "state": status.state,
                "detail": status.detail,
            }
            if status.ready:
                payload["data"] = [{"id": status.model_id, "object": "model", "owned_by": "satya-llama-cpp"}]
            return self._json_response(payload)
        self.send_error(HTTPStatus.NOT_FOUND, "Route not found.")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/v1/chat/completions":
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found.")
            return

        status = MANAGER.status()
        if not status.ready:
            return self._json_response(
                {
                    "error": {
                        "message": status.detail,
                        "type": "model_not_ready",
                        "state": status.state,
                    }
                },
                status=HTTPStatus.SERVICE_UNAVAILABLE,
            )

        payload = self._read_json()
        try:
            response_status, body, content_type = MANAGER.proxy_chat(payload)
            self._write_response(response_status, body, content_type)
        except Exception as exc:
            self._json_response(
                {"error": {"message": f"Gateway proxy error: {exc}", "type": "proxy_error"}},
                status=HTTPStatus.BAD_GATEWAY,
            )

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > MAX_JSON_BODY_BYTES:
            raise ValueError("Invalid JSON request body.")
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw or b"{}")

    def _json_response(self, data: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._write_response(status, json.dumps(data).encode("utf-8"), "application/json; charset=utf-8")

    def _write_response(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()


def run_gateway(host: str = GATEWAY_HOST, port: int = GATEWAY_PORT) -> None:
    MANAGER.ensure_started()
    server = GatewayServer((host, port), GatewayHandler)
    print(f"Satya Sangeet LLM gateway running at http://{host}:{port}/v1", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        MANAGER.stop()
        server.server_close()


if __name__ == "__main__":
    run_gateway()
