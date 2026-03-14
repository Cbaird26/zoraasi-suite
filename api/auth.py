"""
JWT authentication for Zora Middle layer.
When ZORA_LAYER=middle, /query requires Bearer token.
"""

import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY = int(os.getenv("JWT_EXPIRY", "3600"))
MIDDLE_USER = os.getenv("MIDDLE_USER", "chris")
MIDDLE_PASSWORD = os.getenv("MIDDLE_PASSWORD", "")  # Dev only
MIDDLE_PASSWORD_HASH = os.getenv("MIDDLE_PASSWORD_HASH", "")  # Production

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


ZORA_LAYER = os.getenv("ZORA_LAYER", "outer")


def verify_middle_user(username: str, password: str) -> bool:
    """Verify credentials for Middle layer. Use MIDDLE_PASSWORD_HASH in prod."""
    if username != MIDDLE_USER:
        return False
    if MIDDLE_PASSWORD_HASH:
        return verify_password(password, MIDDLE_PASSWORD_HASH)
    if MIDDLE_PASSWORD:  # Dev only
        return password == MIDDLE_PASSWORD
    return False


def create_access_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRY)
    payload = {"sub": sub, "exp": expire, "type": "access"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRY * 24)
    payload = {"sub": sub, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    if not JWT_SECRET:
        return None
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> str | None:
    """Extract and validate Bearer token. Returns username or None if no/invalid token."""
    if not creds or creds.credentials is None:
        return None
    payload = decode_token(creds.credentials)
    if not payload or payload.get("type") != "access":
        return None
    sub = payload.get("sub")
    return str(sub) if sub else None


async def require_auth(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    """Require valid Bearer token. Raises 401 if missing or invalid."""
    if not creds or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(creds.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return str(sub)


async def optional_middle_auth(
    creds: HTTPAuthorizationCredentials | None = Depends(security),
) -> str | None:
    """When ZORA_LAYER=middle: require Bearer token. When outer: return None."""
    if ZORA_LAYER != "middle":
        return None
    return await require_auth(creds)
