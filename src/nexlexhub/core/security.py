from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from time import monotonic
from typing import Any

from fastapi import Depends, Header, HTTPException, status

from nexlexhub.core.config import Settings, get_settings


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, tuple[float, int]] = {}

    def check(self, key: str, limit: int) -> None:
        now = monotonic()
        window_start, count = self._buckets.get(key, (now, 0))
        if now - window_start > 60:
            window_start, count = now, 0
        if count >= limit:
            raise HTTPException(status_code=429, detail="rate limit exceeded")
        self._buckets[key] = (window_start, count + 1)


rate_limiter = InMemoryRateLimiter()


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def hash_password(password: str, salt: str | None = None) -> str:
    salt_value = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_value.encode("utf-8"), 390000)
    return f"{salt_value}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, _ = password_hash.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(hash_password(password, salt), password_hash)


def create_access_token(subject: str, role: str, settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    header = {"alg": "HS256", "typ": "JWT"}
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "role": role,
        "iss": cfg.jwt_issuer,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=cfg.access_token_expiry_minutes)).timestamp()),
    }
    signing_input = ".".join(
        [
            _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8")),
            _b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8")),
        ]
    )
    signature = hmac.new(cfg.jwt_secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url(signature)}"


def decode_access_token(token: str, settings: Settings | None = None) -> dict[str, Any]:
    cfg = settings or get_settings()
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    signing_input = f"{encoded_header}.{encoded_payload}"
    expected_signature = hmac.new(
        cfg.jwt_secret.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(_b64url_decode(encoded_signature), expected_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    payload = json.loads(_b64url_decode(encoded_payload))
    if payload.get("iss") != cfg.jwt_issuer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token issuer")
    if int(payload.get("exp", 0)) < int(datetime.now(UTC).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    return payload


def _allowed_roles() -> dict[str, set[str]]:
    return {
        "reader": {"reader", "analyst", "admin"},
        "analyst": {"analyst", "admin"},
        "admin": {"admin"},
    }


def require_role(required: str) -> Callable:
    async def dependency(
        authorization: str | None = Header(default=None),
        x_api_key: str | None = Header(default=None),
        settings: Settings = Depends(get_settings),
    ) -> dict[str, str]:
        identity: dict[str, str] | None = None
        if authorization and authorization.lower().startswith("bearer "):
            token = authorization.split(" ", 1)[1]
            payload = decode_access_token(token, settings)
            identity = {"subject": str(payload["sub"]), "role": str(payload["role"])}
            rate_limiter.check(identity["subject"], settings.rate_limit_per_minute)
        elif x_api_key:
            role = settings.key_roles().get(x_api_key)
            if role:
                identity = {"subject": x_api_key, "role": role}
                rate_limiter.check(x_api_key, settings.rate_limit_per_minute)
        if identity is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing credentials")
        if identity["role"] not in _allowed_roles().get(required, {required}):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="insufficient role")
        return identity

    return dependency


@asynccontextmanager
async def noop_lifespan() -> AsyncIterator[None]:
    yield
