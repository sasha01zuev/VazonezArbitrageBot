import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from utils.misc.throttling import THROTTLE_LIMITS


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 1.0, key_prefix: str = "antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        self._throttled_users: Dict[str, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        key = f"{self.prefix}{event.from_user.id}"

        limit = THROTTLE_LIMITS.get(id(handler), self.rate_limit)

        now = asyncio.get_event_loop().time()
        last_time = self._throttled_users.get(key, 0)

        if now - last_time < limit:
            await event.answer("⏳ ANTISPAM!")
            return

        self._throttled_users[key] = now
        return await handler(event, data)
