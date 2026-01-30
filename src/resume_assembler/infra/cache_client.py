from __future__ import annotations

from os import getenv

import redis
from utils.types import CacheClient

REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")

_redis: CacheClient | None = None


def get_cache() -> CacheClient:
    global _redis
    if _redis is None:
        _redis = redis.Redis.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            health_check_interval=30,
        )
    return _redis
