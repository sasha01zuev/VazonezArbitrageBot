import asyncio
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable, Optional, Union
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message, CallbackQuery


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, default_limit: float = 1.0, key_prefix: str = "antiflood_"):
        self.default_limit = default_limit
        self.prefix = key_prefix
        self._throttled: Dict[str, float] = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Optional[Any]:

        user_id = None
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return await handler(event, data)

        # Получаем лимит из flags или по умолчанию
        rate_limit = get_flag(data, "throttling_rate_limit", default=self.default_limit)
        key = get_flag(data, "throttling_key", default=f"{self.prefix}{user_id}")

        now = asyncio.get_event_loop().time()
        last_time = self._throttled.get(key, 0)

        # Проверка интервала
        if now - last_time < rate_limit:
            await self.on_throttled(event, rate_limit - (now - last_time))
            return  # Не пускаем дальше

        # Запоминаем время
        self._throttled[key] = now
        return await handler(event, data)

    async def on_throttled(self, event: Union[Message, CallbackQuery], delta: float):
        delta = round(delta, 1)
        try:
            if isinstance(event, Message):
                await event.answer(f"⏳ Подожди {delta} сек...", parse_mode="HTML")
            elif isinstance(event, CallbackQuery):
                await event.answer(f"⏳ Подожди {delta} сек...", show_alert=False)
        except Exception as e:
            print("Error while sending throttling message:", e)

        await asyncio.sleep(delta)
