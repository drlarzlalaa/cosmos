"""COSMOS runtime configuration - env vars only, no config-file parser
needed yet. Stdlib only.
"""
import os
import secrets

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _default_secret_path():
    return os.path.join(ROOT, ".secret_key")


def load_secret_key():
    """COSMOS_SECRET_KEY env var wins. Otherwise reuse (or create) a
    local .secret_key file so tokens issued before a restart stay
    valid - this is a development default, not a production secrets
    story (see infrastructure/secrets-management for that, Phase 8)."""
    env_key = os.environ.get("COSMOS_SECRET_KEY")
    if env_key:
        return env_key
    path = _default_secret_path()
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    key = secrets.token_hex(32)
    with open(path, "w") as f:
        f.write(key)
    return key


class Settings:
    def __init__(self):
        self.db_path = os.environ.get("COSMOS_DB_PATH", os.path.join(ROOT, "data", "cosmos.db"))
        self.host = os.environ.get("COSMOS_HOST", "127.0.0.1")
        self.port = int(os.environ.get("COSMOS_PORT", "8080"))
        self.secret_key = load_secret_key()
        self.frontend_dir = os.path.join(ROOT, "frontend")
        self.token_ttl_seconds = int(os.environ.get("COSMOS_TOKEN_TTL_SECONDS", str(24 * 3600)))
