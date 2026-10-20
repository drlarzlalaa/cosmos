import time
import unittest

import conftest_paths  # noqa: F401  (sets up sys.path)
import auth


class PasswordHashingTests(unittest.TestCase):
    def test_round_trip(self):
        salt_hex, hash_hex = auth.hash_password("correct-horse-battery-staple")
        self.assertTrue(auth.verify_password("correct-horse-battery-staple", salt_hex, hash_hex))

    def test_wrong_password_rejected(self):
        salt_hex, hash_hex = auth.hash_password("correct-horse-battery-staple")
        self.assertFalse(auth.verify_password("wrong-password", salt_hex, hash_hex))

    def test_salts_differ(self):
        salt_a, _ = auth.hash_password("same-password")
        salt_b, _ = auth.hash_password("same-password")
        self.assertNotEqual(salt_a, salt_b)


class TokenTests(unittest.TestCase):
    def test_round_trip(self):
        token = auth.issue_token({"user_id": 42}, "secret", ttl_seconds=60)
        payload = auth.verify_token(token, "secret")
        self.assertEqual(payload["user_id"], 42)

    def test_wrong_secret_rejected(self):
        token = auth.issue_token({"user_id": 42}, "secret", ttl_seconds=60)
        with self.assertRaises(auth.AuthError):
            auth.verify_token(token, "wrong-secret")

    def test_tampered_token_rejected(self):
        token = auth.issue_token({"user_id": 42}, "secret", ttl_seconds=60)
        body_b64, sig_b64 = token.split(".")
        tampered = body_b64 + "x." + sig_b64
        with self.assertRaises(auth.AuthError):
            auth.verify_token(tampered, "secret")

    def test_expired_token_rejected(self):
        token = auth.issue_token({"user_id": 42}, "secret", ttl_seconds=-1)
        time.sleep(0.01)
        with self.assertRaises(auth.AuthError):
            auth.verify_token(token, "secret")

    def test_malformed_token_rejected(self):
        with self.assertRaises(auth.AuthError):
            auth.verify_token("not-a-token", "secret")


if __name__ == "__main__":
    unittest.main()
