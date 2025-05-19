import logging

from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject
from services.database.postgresql import Database  # путь от корня


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logging.debug(f"RegisterUserMiddleware: {event=}, {data=}")

        user = None

        if hasattr(event, "from_user"):
            user = event.from_user

        elif hasattr(event, "message") and hasattr(event.message, "from_user"):
            user = event.message.from_user
        elif hasattr(event, "callback_query") and hasattr(event.callback_query, "from_user"):
            user = event.callback_query.from_user
        elif hasattr(event, "edited_message") and hasattr(event.edited_message, "from_user"):
            user = event.edited_message.from_user
        else:
            logging.warning("User not found in event.")
            return await handler(event, data)

        db: Database = data["db"]

        if not db:
            logging.critical("База данных не инициализирована в workflow_data")
            return await handler(event, data)

        db_user = await db.get_user(user_id=user.id)

        if not db_user:
            await db.add_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                language="ru"
            )
            logging.debug(f"User {user.id} registered in the database.")
        else:
            logging.debug(f"User {user.id} already exists in the database.")

        # TODO: В будущем добавить проверку на другие параметры, например на подписку, настройки и т.д.

        return await handler(event, data)
