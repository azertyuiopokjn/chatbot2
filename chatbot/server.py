"""Minimal HTTP interface for the chatbot using only the standard library."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Optional, Tuple

from .chatbot import ChatSession, load_chatbot


class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, ChatSession] = {}
        self._lock = threading.Lock()

    def get_or_create(self, session_id: Optional[str] = None) -> ChatSession:
        with self._lock:
            if session_id and session_id in self._sessions:
                return self._sessions[session_id]
            chatbot = load_chatbot()
            self._sessions[chatbot.session_id] = chatbot
            return chatbot


store = SessionStore()


class ChatHandler(BaseHTTPRequestHandler):
    server_version = "Chatbot2HTTP/1.0"

    def do_GET(self):
        if self.path.rstrip("/") == "/healthz":
            self._send_json({"status": "ok"})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path.rstrip("/") != "/chat":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        message = payload.get("message")
        if not message:
            self.send_error(400, "Field 'message' is required")
            return

        session = store.get_or_create(payload.get("session_id"))
        reply = session.respond(str(message))
        self._send_json({"reply": reply, "session_id": session.session_id})

    def log_message(self, format: str, *args):  # type: ignore[override]
        return  # Silence default logging

    def _send_json(self, data, status: int = 200):
        encoded = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), ChatHandler)


def serve_in_thread(server: ThreadingHTTPServer) -> Tuple[threading.Thread, ThreadingHTTPServer]:
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread, server


def main():
    server = create_server()
    host, port = server.server_address
    print(f"Chatbot server running on http://{host}:{port}\nPress Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
