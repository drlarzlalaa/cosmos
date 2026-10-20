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

    def _register(self, email):
        _, data = _request("POST", self.base + "/api/auth/register", {
            "email": email, "password": "password123", "display_name": "Researcher",
        })
        return data["token"]

    def test_create_source_requires_auth(self):
        status, data = _request("POST", self.base + "/api/sources", {
            "title": "X", "abstract": "Y", "evidence_status": "speculative",
        })
        self.assertEqual(status, 401)

    def test_create_and_search_source(self):
        token = self._register("source-author@example.com")
        status, data = _request("POST", self.base + "/api/sources", {
            "title": "Gravitational lensing confirms general relativity",
            "abstract": "Light bends around massive bodies, observed during eclipses.",
            "evidence_status": "established",
        }, token=token)
        self.assertEqual(status, 201)
        source_id = data["source"]["id"]

        status, data = _request("GET", self.base + "/api/sources/%d" % source_id)
        self.assertEqual(status, 200)
        self.assertEqual(data["source"]["evidence_status"], "established")

        status, data = _request("GET", self.base + "/api/sources?q=lensing")
        self.assertEqual(status, 200)
        self.assertTrue(any(s["id"] == source_id for s in data["sources"]))

    def test_create_source_rejects_bad_evidence_status(self):
        token = self._register("bad-status@example.com")
        status, data = _request("POST", self.base + "/api/sources", {
            "title": "X", "abstract": "Y", "evidence_status": "definitely-true",
        }, token=token)
        self.assertEqual(status, 400)

    def test_get_unknown_source_404(self):
        status, data = _request("GET", self.base + "/api/sources/999999")
        self.assertEqual(status, 404)

    def test_gravity_calculation_no_auth_required(self):
        status, data = _request("POST", self.base + "/api/engines/gravity", {
            "calculation": "force", "inputs": {"mass1_kg": 1000, "mass2_kg": 1000, "distance_m": 1},
        })
        self.assertEqual(status, 200)
        self.assertEqual(data["evidence_status"], "established")

    def test_gravity_unknown_calculation_rejected(self):
        status, data = _request("POST", self.base + "/api/engines/gravity", {
            "calculation": "teleportation", "inputs": {},
        })
        self.assertEqual(status, 400)

    def test_gravity_calculations_listing(self):
        status, data = _request("GET", self.base + "/api/engines/gravity")
        self.assertEqual(status, 200)
        self.assertIn("force", data["calculations"])


if __name__ == "__main__":
    unittest.main()
