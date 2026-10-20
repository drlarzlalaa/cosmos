"""Import this first in every test module - puts the hyphenated
backend module directories on sys.path. Named conftest_paths (not
conftest.py) because there's no pytest on the build machine; tests
run with stdlib unittest.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import cosmos_paths  # noqa: E402

cosmos_paths.add_backend_paths(ROOT)
