from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from time import monotonic

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


def require_role(required: str) -> Callable:
    async def dependency(
        x_api_key: str = Header(default=""),
        settings: Settings = Depends(get_settings),
    ) -> dict[str, str]:
        roles = settings.key_roles()
        role = roles.get(x_api_key)
        if not role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
        rate_limiter.check(x_api_key, settings.rate_limit_per_minute)
        allowed = {"reader": {"reader"}, "analyst": {"reader", "analyst"}, "admin": {"reader", "analyst", "admin"}}
        if required not in allowed.get(role, {role}) and role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="insufficient role")
        return {"api_key": x_api_key, "role": role}

    return dependency


@asynccontextmanager
async def noop_lifespan() -> AsyncIterator[None]:
    yield
