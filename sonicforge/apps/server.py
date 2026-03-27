from __future__ import annotations

import errno
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from sonicforge.core.academy_ai import academy_llm_status, coach_academy_user
from sonicforge.core.academy_stt import transcribe_audio_base64
from sonicforge.core.academy_tts import synthesize_academy_speech
from sonicforge.core.models import project_from_dict
from sonicforge.core.session import (
    apply_mix,
    apply_project_suggestion,
    create_project,
    render_project_audio,
)


WEB_ROOT = Path(__file__).resolve().parents[1] / "web"
MAX_JSON_BODY_BYTES = 8 * 1024 * 1024
CLIENT_DISCONNECT_ERRNOS = {errno.EPIPE, errno.ECONNRESET}


class SonicForgeHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class SonicForgeHandler(BaseHTTPRequestHandler):
    server_version = "SonicForgeHTTP/0.1"

    def do_OPTIONS(self) -> None:
        self._write_response(HTTPStatus.NO_CONTENT, b"")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/", "/harmonium", "/index.html"}:
            return self._serve_file("harmonium.html", "text/html; charset=utf-8")
        if path in {"/academy", "/harmonium-docs", "/documentation"}:
            return self._serve_file("harmonium_docs.html", "text/html; charset=utf-8")
        if path == "/api/health":
            return self._json_response({"status": "ok", "app": "SonicForge X MVP"})
        if path == "/api/academy-llm-status":
            return self._json_response(academy_llm_status())
        static_path = WEB_ROOT / path.lstrip("/")
        if static_path.exists() and static_path.is_file():
            content_type, _ = mimetypes.guess_type(static_path.name)
            return self._serve_file(static_path.name, content_type or "application/octet-stream")
        self.send_error(HTTPStatus.NOT_FOUND, "Route not found.")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/compose":
                project = create_project(
                    name=payload.get("name", "Untitled Forge Session"),
                    genre=payload.get("genre", "cinematic-electronic"),
                    tempo=int(payload.get("tempo", 118)),
                    bars=int(payload.get("bars", 8)),
                    valence=float(payload.get("valence", 55)),
                    energy=float(payload.get("energy", 60)),
                    tension=float(payload.get("tension", 45)),
                    lyrics=payload.get("lyrics", ""),
                    seed=payload.get("seed"),
                )
                return self._json_response(project.to_dict())
            if path == "/api/auto-mix":
                project = apply_mix(project_from_dict(payload["project"]))
                return self._json_response(project.to_dict())
            if path == "/api/apply-suggestion":
                project = apply_project_suggestion(
                    project_from_dict(payload["project"]),
                    payload["suggestion_id"],
                )
                return self._json_response(project.to_dict())
            if path == "/api/export-wav":
                project = project_from_dict(payload["project"])
                wav_bytes = render_project_audio(project)
                self._write_response(
                    HTTPStatus.OK,
                    wav_bytes,
                    content_type="audio/wav",
                    extra_headers={"Content-Disposition": f'attachment; filename="{project.name}.wav"'},
                )
                return None
            if path == "/api/academy-assistant":
                return self._json_response(coach_academy_user(payload))
            if path == "/api/academy-tts":
                render = synthesize_academy_speech(
                    payload.get("text", ""),
                    payload.get("language", "en-IN"),
                    payload.get("voice_style", ""),
                )
                self._write_response(
                    HTTPStatus.OK,
                    render.audio_bytes,
                    content_type=render.content_type,
                    extra_headers={
                        "X-SNSAI-Voice": render.voice_name,
                        "X-SNSAI-TTS-Provider": render.provider,
                    },
                )
                return None
            if path == "/api/academy-transcribe":
                return self._json_response(
                    transcribe_audio_base64(
                        payload.get("audio_base64", ""),
                        payload.get("mime_type", "audio/webm"),
                        payload.get("language", ""),
                    )
                )
            self.send_error(HTTPStatus.NOT_FOUND, "Route not found.")
        except OSError as exc:
            if self._client_disconnected(exc):
                return None
            raise
        except ValueError as exc:
            return self._json_response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
        except Exception as exc:  # pragma: no cover - defensive API guard
            return self._json_response({"error": f"Assistant server error: {exc}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def log_message(self, fmt: str, *args) -> None:
        return None

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid Content-Length header.") from exc
        if length < 0:
            raise ValueError("Invalid Content-Length header.")
        if length > MAX_JSON_BODY_BYTES:
            raise ValueError("Request body is too large.")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw or b"{}")
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON request body.") from exc

    def _json_response(self, data: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(data).encode("utf-8")
        self._write_response(status, encoded, content_type="application/json; charset=utf-8")

    def _serve_file(self, filename: str, content_type: str) -> None:
        asset = WEB_ROOT / filename
        if not asset.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found.")
            return None
        body = asset.read_bytes()
        self._write_response(HTTPStatus.OK, body, content_type=content_type)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _client_disconnected(self, exc: OSError) -> bool:
        return isinstance(exc, (BrokenPipeError, ConnectionResetError)) or exc.errno in CLIENT_DISCONNECT_ERRNOS

    def _write_response(
        self,
        status: HTTPStatus,
        body: bytes,
        *,
        content_type: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> bool:
        try:
            self.send_response(status)
            self._send_cors_headers()
            if content_type:
                self.send_header("Content-Type", content_type)
            if extra_headers:
                for key, value in extra_headers.items():
                    self.send_header(key, value)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)
            return True
        except OSError as exc:
            if self._client_disconnected(exc):
                return False
            raise


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = SonicForgeHTTPServer((host, port), SonicForgeHandler)
    print(f"SonicForge X web app running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
