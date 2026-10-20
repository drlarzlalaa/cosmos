"""COSMOS API gateway - Phase 1: accounts + static frontend only.
Stdlib http.server, no framework installed on the build machine.
Routing is a short explicit table, not a generic router, because the
route count is still small; revisit if/when later phases add many
more endpoints.
"""
import json
import mimetypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import auth
import db
import users

PHASE = 1


def make_handler(settings):
    def current_store():
        # sqlite3 connections can't cross threads; db.get_connection()
        # caches one per (db_path, thread id), so fetching it lazily
        # here (rather than once at server start-up) keeps every
        # request on a connection owned by the thread handling it.
        return users.UserStore(db.get_connection(settings.db_path))

    class Handler(BaseHTTPRequestHandler):
        server_version = "COSMOS/0.1"

        def log_message(self, fmt, *args):
            pass  # keep test/CI output quiet; errors still raise

        def _send_json(self, status, body):
            payload = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _read_json_body(self):
            length = int(self.headers.get("Content-Length", "0"))
            if length == 0:
                return {}
            raw = self.rfile.read(length)
            try:
                return json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                raise ValueError("invalid JSON body")

        def _current_user(self):
            header = self.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return None
            token = header[len("Bearer "):]
            try:
                payload = auth.verify_token(token, settings.secret_key)
            except auth.AuthError:
                return None
            return current_store().get_by_id(payload.get("user_id"))

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/api/health":
                return self._send_json(200, {"status": "ok", "phase": PHASE})
            if path == "/api/users/me":
                user = self._current_user()
                if user is None:
                    return self._send_json(401, {"error": "not authenticated"})
                return self._send_json(200, {"user": user})
            if path.startswith("/api/"):
                return self._send_json(404, {"error": "not found"})
            return self._serve_static(path)

        def do_POST(self):
            path = urlparse(self.path).path
            try:
                body = self._read_json_body()
            except ValueError as exc:
                return self._send_json(400, {"error": str(exc)})

            if path == "/api/auth/register":
                return self._handle_register(body)
            if path == "/api/auth/login":
                return self._handle_login(body)
            return self._send_json(404, {"error": "not found"})

        def _handle_register(self, body):
            try:
                user = current_store().create_user(
                    body.get("email", ""), body.get("password", ""),
                    body.get("display_name", ""),
                )
            except users.UserError as exc:
                return self._send_json(400, {"error": str(exc)})
            token = auth.issue_token({"user_id": user["id"]}, settings.secret_key, settings.token_ttl_seconds)
            return self._send_json(201, {"user": user, "token": token})

        def _handle_login(self, body):
            try:
                user = current_store().verify_login(body.get("email", ""), body.get("password", ""))
            except users.UserError as exc:
                return self._send_json(401, {"error": str(exc)})
            token = auth.issue_token({"user_id": user["id"]}, settings.secret_key, settings.token_ttl_seconds)
            return self._send_json(200, {"user": user, "token": token})

        def _serve_static(self, path):
            if path == "/":
                path = "/login/"
            if path.endswith("/"):
                path += "index.html"
            safe_path = os.path.normpath(path).lstrip("/")
            full_path = os.path.join(settings.frontend_dir, safe_path)
            if not full_path.startswith(os.path.abspath(settings.frontend_dir)):
                return self._send_json(403, {"error": "forbidden"})
            if not os.path.isfile(full_path):
                return self._send_json(404, {"error": "not found"})
            content_type = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
            with open(full_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    return Handler


def build_server(settings):
    """A single-threaded HTTPServer - sqlite3 connections are not safe
    to share across threads, and Phase 1 has no concurrency
    requirement that would justify the extra complexity of a
    per-thread connection pool. Revisit if/when real concurrent load
    shows up."""
    handler = make_handler(settings)
    return HTTPServer((settings.host, settings.port), handler)


def run_in_thread(settings):
    """Used by tests: starts the server on its configured port in a
    background thread and returns it so the caller can shut it down."""
    httpd = build_server(settings)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, thread
