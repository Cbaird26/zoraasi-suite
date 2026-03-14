"""Unit tests for auth module."""

import os

# Set JWT_SECRET before importing auth (module reads env at import)
os.environ.setdefault("JWT_SECRET", "test-secret-for-ci")

import pytest
from auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_middle_user,
    verify_password,
)


def test_hash_and_verify_password():
    plain = "test123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_decode_access_token():
    token = create_access_token("chris")
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == "chris"
    assert payload.get("type") == "access"


def test_create_and_decode_refresh_token():
    token = create_refresh_token("chris")
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == "chris"
    assert payload.get("type") == "refresh"


def test_verify_middle_user_plain(monkeypatch):
    monkeypatch.setenv("MIDDLE_USER", "chris")
    monkeypatch.setenv("MIDDLE_PASSWORD", "secret")
    monkeypatch.delenv("MIDDLE_PASSWORD_HASH", raising=False)
    # Reload to pick up env
    import importlib
    import auth as auth_mod
    importlib.reload(auth_mod)
    assert auth_mod.verify_middle_user("chris", "secret")
    assert not auth_mod.verify_middle_user("chris", "wrong")
    assert not auth_mod.verify_middle_user("other", "secret")
