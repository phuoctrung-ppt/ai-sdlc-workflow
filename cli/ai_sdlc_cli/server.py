"""localhost office UI — Minecraft-style department floor + token audit."""

from __future__ import annotations

import json
import mimetypes
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ai_sdlc_cli.agents import discover_agents
from ai_sdlc_cli.events import read_benchmarks, read_config, read_events, read_state

STATIC_DIR = Path(__file__).resolve().parent / "static"


def make_handler(work_root: Path):
    class OfficeHandler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:
            if args and str(args[0]).startswith("200"):
                return
            super().log_message(fmt, *args)

        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, data: object) -> None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self._send(code, body, "application/json; charset=utf-8")

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path

            if path in ("/", "/index.html"):
                self._send(200, (STATIC_DIR / "office.html").read_bytes(), "text/html; charset=utf-8")
                return

            if path.startswith("/static/"):
                rel = path[len("/static/") :]
                file_path = (STATIC_DIR / rel).resolve()
                if not str(file_path).startswith(str(STATIC_DIR.resolve())):
                    self._json(403, {"error": "forbidden"})
                    return
                if not file_path.is_file():
                    self._json(404, {"error": "not found"})
                    return
                ctype = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
                self._send(200, file_path.read_bytes(), ctype)
                return

            if path == "/api/snapshot":
                self._json(
                    200,
                    {
                        "work_root": str(work_root),
                        "config": read_config(work_root),
                        "agents": discover_agents(work_root),
                        "state": read_state(work_root),
                        "benchmarks": read_benchmarks(work_root),
                    },
                )
                return

            if path == "/api/benchmarks":
                self._json(200, read_benchmarks(work_root))
                return

            if path == "/api/events":
                qs = parse_qs(parsed.query)
                after = int(qs.get("after", ["0"])[0] or 0)
                events, cursor = read_events(work_root, after_line=after)
                self._json(200, {"events": events, "cursor": cursor})
                return

            if path == "/api/stream":
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()
                qs = parse_qs(parsed.query)
                cursor = int(qs.get("after", ["0"])[0] or 0)
                try:
                    while True:
                        events, cursor = read_events(work_root, after_line=cursor, limit=50)
                        if events:
                            payload = json.dumps(
                                {
                                    "events": events,
                                    "cursor": cursor,
                                    "state": read_state(work_root),
                                    "benchmarks": read_benchmarks(work_root),
                                },
                                ensure_ascii=False,
                            )
                            self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
                            self.wfile.flush()
                        else:
                            self.wfile.write(b": ping\n\n")
                            self.wfile.flush()
                        time.sleep(1.0)
                except (BrokenPipeError, ConnectionResetError):
                    return

            self._json(404, {"error": "not found", "path": path})

    return OfficeHandler


def serve(work_root: Path, host: str = "127.0.0.1", port: int = 9669) -> None:
    work_root = work_root.resolve()
    handler = make_handler(work_root)
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"ai-sdlc office UI → http://{host}:{port}")
    print(f"work root        → {work_root}")
    print("Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
        httpd.server_close()
