from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from utils.misc.throttling import rate_limit

start_router = Router()


@start_router.message(CommandStart())
@rate_limit(limit=2)  # Anti-spam
async def start_handler(message: Message):
    await message.answer("Start Command")