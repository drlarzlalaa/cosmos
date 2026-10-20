#!/usr/bin/env python3
"""Start the COSMOS API gateway (Phase 1: accounts + static frontend).

Module directories under backend/ and storage/ use hyphens to match
ARCHITECTURE.md's naming (api-gateway, relational-database, ...), which
Python can't import as dotted packages - so this entry point adds each
directory straight to sys.path and imports its (hyphen-free) .py files
by bare module name instead. Every other script in this repo that needs
to cross these boundaries (tests, tools) does the same thing via
cosmos_paths.add_backend_paths().
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import cosmos_paths  # noqa: E402

cosmos_paths.add_backend_paths(ROOT)

import server  # noqa: E402
import settings as settings_module  # noqa: E402


def main():
    settings = settings_module.Settings()
    httpd = server.build_server(settings)
    print("COSMOS Phase 1 gateway listening on http://%s:%d/" % (settings.host, settings.port))
    print("  -> open http://%s:%d/login/ to register or sign in" % (settings.host, settings.port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
        httpd.shutdown()


if __name__ == "__main__":
    main()
