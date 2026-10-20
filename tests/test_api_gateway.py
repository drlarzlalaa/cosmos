import json
import os
import tempfile
import unittest
import urllib.error
import urllib.request

import conftest_paths  # noqa: F401
import server
import settings as settings_module


def _request(method, url, body=None, token=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


class ApiGatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.mkdtemp()
        settings = settings_module.Settings()
        settings.db_path = os.path.join(cls.tmp_dir, "gateway.db")
        settings.host = "127.0.0.1"
        settings.port = 0  # OS picks a free port
        settings.secret_key = "test-secret"
        cls.httpd, cls.thread = server.run_in_thread(settings)
        cls.port = cls.httpd.server_address[1]
        cls.base = "http://127.0.0.1:%d" % cls.port

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()

    def test_health(self):
        status, data = _request("GET", self.base + "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")

    def test_register_login_and_me(self):
        status, data = _request("POST", self.base + "/api/auth/register", {
            "email": "pip@example.com", "password": "password123", "display_name": "Pip",
        })
        self.assertEqual(status, 201)
        token = data["token"]

        status, data = _request("GET", self.base + "/api/users/me", token=token)
        self.assertEqual(status, 200)
        self.assertEqual(data["user"]["email"], "pip@example.com")

        status, data = _request("POST", self.base + "/api/auth/login", {
            "email": "pip@example.com", "password": "password123",
        })
        self.assertEqual(status, 200)
        self.assertTrue(data["token"])

    def test_me_without_token_rejected(self):
        status, data = _request("GET", self.base + "/api/users/me")
        self.assertEqual(status, 401)

    def test_login_wrong_password_rejected(self):
        _request("POST", self.base + "/api/auth/register", {
            "email": "bit@example.com", "password": "password123", "display_name": "Bit",
        })
        status, data = _request("POST", self.base + "/api/auth/login", {
            "email": "bit@example.com", "password": "wrong-password",
        })
        self.assertEqual(status, 401)

    def test_login_page_served(self):
        with urllib.request.urlopen(self.base + "/login/") as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn(b"COSMOS", resp.read())


if __name__ == "__main__":
    unittest.main()
