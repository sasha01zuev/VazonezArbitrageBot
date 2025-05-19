from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery
from typing import Callable, Awaitable, Any, Dict, Union
import logging


class DebugLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery, InlineQuery],
        data: Dict[str, Any],
    ) -> Any:
        try:
            user = event.from_user
            user_repr = f"[{user.id}] @{user.username or user.full_name}"

            if isinstance(event, Message):
                if event.edit_date:
                    logging.debug(f"✏️ {event.__class__.__name__} от {user_repr}: {event.text}")
                else:
                    logging.debug(f"📩 {event.__class__.__name__} от {user_repr}: {event.text}")
            elif isinstance(event, CallbackQuery):
                logging.debug(f"🔘 {event.__class__.__name__} от {user_repr}: {event.data}")
            elif isinstance(event, InlineQuery):
                logging.debug(f"🔎 {event.__class__.__name__} от {user_repr}: {event.query}")
            else:
                logging.debug(f"🌀 {event.__class__.__name__} от {user_repr}: {event}")
        except Exception as e:
            logging.exception(f"‼️ Ошибка в DebugLoggerMiddleware: {e}")

        return await handler(event, data)
