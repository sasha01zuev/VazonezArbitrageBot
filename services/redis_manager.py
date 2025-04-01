import json
from typing import Dict, Any
from redis.asyncio import Redis
from typing import Tuple
import os


class RedisArbitrageManager:
    def __init__(self, host: str = None, port: int = 6379, db: int = 0):
        redis_host = host or os.getenv("REDIS_HOST", "localhost")
        self.redis = Redis(host=redis_host, port=port, db=db, decode_responses=True)

    async def get_all_pairs(self) -> Dict[str, Dict[str, Any]]:
        keys = await self.redis.keys("*:*:*")
        result = {}
        for key in keys:
            # ttl = await self.redis.ttl(key)
            # print(key, ttl)
            value = await self.redis.get(key)
            if value:
                result[key] = json.loads(value)
        return result

    async def get_pair(self, exchange1: str, exchange2: str, coin: str) -> Tuple[dict | None, int | None]:
        key = f"{exchange1}:{exchange2}:{coin}"
        value = await self.redis.get(key)
        ttl = await self.redis.ttl(key)
        return json.loads(value) if value else None, ttl

