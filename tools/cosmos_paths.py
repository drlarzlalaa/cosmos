"""Shared helper: put every hyphenated COSMOS module directory that
Phase 1 code needs onto sys.path, once, in dependency order. See the
docstring in run.py for why this exists instead of normal package
imports.
"""
import os
import sys

_BACKEND_DIRS = [
    "storage/relational-database",
    "backend/configuration",
    "backend/authentication",
    "backend/user-management",
    "backend/api-gateway",
]


def add_backend_paths(root):
    for rel_dir in _BACKEND_DIRS:
        full_dir = os.path.join(root, rel_dir)
        if full_dir not in sys.path:
            sys.path.insert(0, full_dir)
