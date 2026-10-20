import os
import tempfile
import unittest

import conftest_paths  # noqa: F401
import db
import users


class UserStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test.db")
        self.conn = db.get_connection(self.db_path)
        self.store = users.UserStore(self.conn)

    def test_create_and_login(self):
        created = self.store.create_user("Nova@Example.com", "password123", "Nova")
        self.assertEqual(created["email"], "nova@example.com")
        logged_in = self.store.verify_login("nova@example.com", "password123")
        self.assertEqual(logged_in["id"], created["id"])

    def test_duplicate_email_rejected(self):
        self.store.create_user("nova@example.com", "password123", "Nova")
        with self.assertRaises(users.UserError):
            self.store.create_user("nova@example.com", "different-pass", "Nova Two")

    def test_invalid_email_rejected(self):
        with self.assertRaises(users.UserError):
            self.store.create_user("not-an-email", "password123", "Nova")

    def test_short_password_rejected(self):
        with self.assertRaises(users.UserError):
            self.store.create_user("nova@example.com", "short", "Nova")

    def test_wrong_password_rejected(self):
        self.store.create_user("nova@example.com", "password123", "Nova")
        with self.assertRaises(users.UserError):
            self.store.verify_login("nova@example.com", "wrong-password")

    def test_unknown_email_rejected(self):
        with self.assertRaises(users.UserError):
            self.store.verify_login("ghost@example.com", "whatever123")

    def test_default_display_name(self):
        created = self.store.create_user("nova@example.com", "password123", "   ")
        self.assertEqual(created["display_name"], "nova")


if __name__ == "__main__":
    unittest.main()
