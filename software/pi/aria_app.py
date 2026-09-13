"""ARIA local touchscreen app: python aria_app.py --data-dir /path/to/private/data."""
import argparse
import json
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from aria_assistant import AppError, Assistant, Store
from aria_voice import Voice


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, assistant):
        self.assistant = assistant
        self.token = secrets.token_urlsafe(32)
        self.assets = Path(__file__).parent / "app_ui"
        super().__init__(address, Handler)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # Do not log personal conversation or HTTP request bodies.

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def valid_host(self):
        return self.headers.get("Host") == f"127.0.0.1:{self.server.server_port}"

    def send(self, code, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, ensure_ascii=False, allow_nan=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        try:
            self.wfile.write(body)
        except OSError:
            pass  # Client closed the page while a response was being sent.

    def do_GET(self):
        if not self.valid_host():
            return self.send(403, {"error": "Host không hợp lệ."})
        path = urlsplit(self.path).path
        if path == "/api/state":
            if self.headers.get("Origin") not in (None, f"http://127.0.0.1:{self.server.server_port}"):
                return self.send(403, {"error": "Nguồn yêu cầu không hợp lệ."})
            state = self.server.assistant.snapshot()
            state["token"] = self.server.token
            return self.send(200, state)
        assets = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                  "/style.css": ("style.css", "text/css")}
        if path not in assets:
            return self.send(404, {"error": "Không tìm thấy."})
        name, mime = assets[path]
        self.send(200, (self.server.assets / name).read_bytes(), mime + "; charset=utf-8")

    def do_POST(self):
        expected_origin = f"http://127.0.0.1:{self.server.server_port}"
        if (not self.valid_host() or self.headers.get("Origin") != expected_origin
                or self.headers.get("X-ARIA-Token") != self.server.token):
            return self.send(403, {"error": "Phiên không hợp lệ; tải lại app."})
        if self.headers.get("Content-Type") != "application/json":
            return self.send(415, {"error": "Yêu cầu JSON."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384 or self.headers.get("Transfer-Encoding"):
                raise AppError("Yêu cầu quá lớn hoặc không hợp lệ.")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise AppError("Yêu cầu cần là một đối tượng JSON.")
            action = self.path.removeprefix("/api/")
            if self.path != "/api/" + action:
                raise AppError("Đường dẫn không hợp lệ.")
            if action == "chat":
                self.server.assistant.start(data.get("text"))
            elif action == "listen":
                self.server.assistant.start(listen=True)
            else:
                self.server.assistant.change(action, data)
            self.send(200, {"ok": True})
        except (AppError, ValueError, UnicodeError) as exc:
            self.send(400, {"error": str(exc) if isinstance(exc, AppError) else "JSON không hợp lệ."})
        except OSError:
            self.close_connection = True


def main():
    parser = argparse.ArgumentParser(description="ARIA touchscreen + Vietnamese dialogue, no motor access")
    parser.add_argument("--data-dir", required=True, type=Path, help="Private local memory/audio directory")
    parser.add_argument("--sensor-snapshot", type=Path, help="Optional fresh JSON sample; app never opens I2C")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("port must be 1024..65535")
    store = Store(args.data_dir)
    voice = Voice(store.path.parent)
    server = Server(("127.0.0.1", args.port), Assistant(store, voice=voice, sensor_path=args.sensor_snapshot))
    print(f"ARIA: http://127.0.0.1:{args.port} — local app; motor paused", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.assistant.change("cancel", {})
        if server.assistant.worker:
            server.assistant.worker.join(timeout=3)
        server.server_close()


if __name__ == "__main__":
    main()
