import logging
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import TelegramObject
from services.database.postgresql import Database


class BlacklistMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = None
        if hasattr(event, "from_user"):
            user = event.from_user
        elif hasattr(event, "message") and hasattr(event.message, "from_user"):
            user = event.message.from_user
        elif hasattr(event, "callback_query") and hasattr(event.callback_query, "from_user"):
            user = event.callback_query.from_user
        elif hasattr(event, "edited_message") and hasattr(event.edited_message, "from_user"):
            user = event.edited_message.from_user

        db: Database = data.get("db")
        is_banned = await db.get_user_from_blacklist(user.id)

        if is_banned:
            raise CancelHandler()

        return await handler(event, data)