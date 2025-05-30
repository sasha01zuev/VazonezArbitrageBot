from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
import logging

from keyboards.inline import get_main_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy

start_router = Router()


@start_router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
            disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await message.answer(text=texts.commands.start.welcome,
        disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_main_keyboard(texts=texts))