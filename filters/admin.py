from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import config


class IsMainAdmin(BaseFilter):
    async def __call__(self, obj: Message) -> bool:
        return obj.from_user.id == config.MAIN_ADMIN


class IsAdmin(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return (str(obj.from_user.id) in config.ADMINS_ID) == self.is_admin
