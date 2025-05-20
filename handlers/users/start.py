from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import logging

from services.database.postgresql import Database
from utils.i18n import TextProxy

start_router = Router()


@start_router.message(CommandStart())
async def start_handler(message: Message, db: Database, texts: TextProxy):
    await message.answer(text=texts.start.welcome,
        disable_web_page_preview=True, parse_mode="HTML")