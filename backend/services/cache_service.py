import json

import redis

from config.settings import settings


class CacheService:
    def __init__(self) -> None:
        self.client = None
        try:
            self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
            self.client.ping()
        except Exception:
            self.client = None

    def get_json(self, key: str):
        if not self.client:
            return None
        raw = self.client.get(key)
        if not raw:
            return None
        return json.loads(raw)

    def set_json(self, key: str, value: dict, ttl_seconds: int) -> None:
        if not self.client:
            return
        self.client.setex(key, ttl_seconds, json.dumps(value))


cache_service = CacheService()
