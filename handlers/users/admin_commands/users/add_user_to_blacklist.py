from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import IsMainAdmin

admin_users_router = Router()


@admin_users_router.message(Command("autb"), IsMainAdmin())
async def add_user_to_blacklist(message: Message):
    # await message.bot.send_message("@channel", "Пост от админа")
    await message.answer("✅ Пользователь добавлен в черный список")