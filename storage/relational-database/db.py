"""Thin sqlite3 wrapper for COSMOS's relational-database module.

Stdlib only (sqlite3 is in the standard library) - no ORM, no driver
install needed. Phase 1 scope: just enough to back the users table;
later phases add more tables to schema.sql and this module grows with
them rather than being replaced.
"""
import os
import sqlite3
import threading

_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
_SCHEMA_VERSION = 1

_lock = threading.Lock()
_connections = {}


def get_connection(db_path):
    """One sqlite3 connection per db_path per thread (sqlite3 connections
    are not safe to share across threads)."""
    key = (db_path, threading.get_ident())
    with _lock:
        conn = _connections.get(key)
        if conn is None:
            os.makedirs(os.path.dirname(os.path.abspath(db_path)) or ".", exist_ok=True)
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            _connections[key] = conn
            _init_schema(conn)
    return conn


def _init_schema(conn):
    with open(_SCHEMA_PATH) as f:
        conn.executescript(f.read())
    row = conn.execute("SELECT version FROM schema_version").fetchone()
    if row is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (_SCHEMA_VERSION,))
        conn.commit()
