from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from os import getenv
from time import sleep, time
from typing import Any
from uuid import uuid4

from redis import Redis

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")

_redis: Redis | None = None


def get_cache() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            health_check_interval=30,
        )
    return _redis


RELEASE_LUA = """
if redis.call("GET", KEYS[1]) == ARGV[1] then
  return redis.call("DEL", KEYS[1])
else
  return 0
end
"""


@dataclass(kw_only=True)
class LockAquisitionResult:
    success: bool
    code: int
    message: str

    def __bool__(self):
        return self.success


class ProcessLockHandler:
    redis_client: Redis
    ttl_seconds: int

    def __init__(self, ttl_seconds: int = 60):
        self.redis_client = get_cache()
        self.ttl_seconds = ttl_seconds

    def _get_lock_key(self, user_id: str, process_id: str) -> str:
        return f"lock:resume:{user_id}:{process_id}"

    def _try_acquire(
        self,
        user_id: str,
        process_id: str,
    ) -> str | None:
        key = self._get_lock_key(user_id, process_id)
        token = uuid4().hex
        ok = self.redis_client.set(key, token, nx=True, ex=self.ttl_seconds)
        return token if ok else None

    def _release(
        self,
        user_id: str,
        process_id: str,
        token: str,
    ) -> bool:
        key = self._get_lock_key(user_id, process_id)
        released = self.redis_client.eval(
            RELEASE_LUA,
            1,
            key,
            token,
        )
        return released == 1

    @contextmanager
    def acquire(
        self,
        user_id: str,
        process_id: str,
        wait_seconds: float = 2.0,
        retry_interval: float = 0.05,
    ) -> Generator[None, Any, None]:
        deadline = time() + wait_seconds
        token = None

        while time() < deadline:
            token = self._try_acquire(user_id, process_id)

            if token:
                break
            sleep(retry_interval)

        if not token:
            raise RuntimeError(
                f"Could not acquire lock for {user_id} - {process_id}. Process is likely busy."
            )

        try:
            yield
        finally:
            release = self._release(user_id, process_id, token)
            if not release:
                pass
