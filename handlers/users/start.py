from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Start Command")