"""User accounts for COSMOS, backed by storage/relational-database.
Depends on auth.py (password hashing) - caller wires both in via
sys.path, see run.py.
"""
import re
import sqlite3
import time

import auth

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserError(Exception):
    pass


class UserStore:
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, email, password, display_name):
        email = email.strip().lower()
        if not _EMAIL_RE.match(email):
            raise UserError("invalid email")
        if len(password) < 8:
            raise UserError("password must be at least 8 characters")
        display_name = display_name.strip() or email.split("@")[0]
        salt_hex, hash_hex = auth.hash_password(password)
        try:
            cur = self.conn.execute(
                "INSERT INTO users (email, display_name, password_salt, password_hash, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (email, display_name, salt_hex, hash_hex, _now_iso()),
            )
        except sqlite3.IntegrityError:
            raise UserError("an account with that email already exists")
        self.conn.commit()
        return self.get_by_id(cur.lastrowid)

    def get_by_id(self, user_id):
        row = self.conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return _row_to_public(row) if row else None

    def get_by_email(self, email):
        row = self.conn.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
        return row

    def verify_login(self, email, password):
        row = self.get_by_email(email)
        if row is None:
            raise UserError("invalid email or password")
        if not auth.verify_password(password, row["password_salt"], row["password_hash"]):
            raise UserError("invalid email or password")
        return _row_to_public(row)


def _row_to_public(row):
    return {"id": row["id"], "email": row["email"], "display_name": row["display_name"],
            "created_at": row["created_at"]}


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
