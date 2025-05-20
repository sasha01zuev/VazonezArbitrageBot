import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any
from services.database.postgresql import Database
from utils.i18n import TextProxy
from utils.texts import TEXTS


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user = None
        lang = "ru"

        if hasattr(event, "from_user"):
            user = event.from_user
        elif hasattr(event, "message") and hasattr(event.message, "from_user"):
            user = event.message.from_user
        elif hasattr(event, "callback_query") and hasattr(event.callback_query, "from_user"):
            user = event.callback_query.from_user
        elif hasattr(event, "edited_message") and hasattr(event.edited_message, "from_user"):
            user = event.edited_message.from_user

        db: Database = data.get("db")

        if user and db:
            user_data = await db.get_user(user.id)
            if user_data and "language" in user_data:
                lang = user_data["language"]
                logging.debug(f"Пользователь {user.id} язык: {lang}")
            else:
                # Если язык не найден, можно установить язык по умолчанию
                lang = "ru"
                logging.debug(f"Пользователь {user.id} язык по умолчанию: {lang}")
        else:
            logging.warning("База данных не инициализирована в workflow_data или пользователь не найден.")
            # Если база данных не инициализирована, устанавливаем язык по умолчанию
            lang = "ru"

        data["texts"] = TextProxy(TEXTS, lang=lang)
        return await handler(event, data)
