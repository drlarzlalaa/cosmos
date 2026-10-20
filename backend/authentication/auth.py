"""Password hashing and signed tokens for COSMOS. Stdlib only:
hashlib.pbkdf2_hmac for passwords, hmac+base64+json for tokens
(a minimal JWT-like scheme - no external jwt library installed on
the build machine, and this is honest about not being full JWT).
"""
import base64
import hashlib
import hmac
import json
import os
import time

PBKDF2_ITERATIONS = 200_000


class AuthError(Exception):
    pass


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return salt.hex(), digest.hex()


def verify_password(password, salt_hex, hash_hex):
    _, candidate_hash = hash_password(password, salt_hex)
    return hmac.compare_digest(candidate_hash, hash_hex)


def _b64url_encode(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).rstrip(b"=").decode("ascii")


def _b64url_decode(text):
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def issue_token(payload, secret_key, ttl_seconds):
    body = dict(payload)
    body["exp"] = int(time.time()) + ttl_seconds
    body_bytes = json.dumps(body, separators=(",", ":"), sort_keys=True).encode("utf-8")
    body_b64 = _b64url_encode(body_bytes)
    signature = hmac.new(secret_key.encode("utf-8"), body_b64.encode("ascii"), hashlib.sha256).digest()
    return "%s.%s" % (body_b64, _b64url_encode(signature))


def verify_token(token, secret_key):
    try:
        body_b64, sig_b64 = token.split(".", 1)
    except ValueError:
        raise AuthError("malformed token")
    expected_sig = hmac.new(secret_key.encode("utf-8"), body_b64.encode("ascii"), hashlib.sha256).digest()
    actual_sig = _b64url_decode(sig_b64)
    if not hmac.compare_digest(expected_sig, actual_sig):
        raise AuthError("bad signature")
    payload = json.loads(_b64url_decode(body_b64))
    if payload.get("exp", 0) < time.time():
        raise AuthError("token expired")
    return payload
