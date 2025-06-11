from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_arbitrage_menu_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy

arbitrage_menu_router = Router()


@arbitrage_menu_router.message(Command("arbitrage"), StateFilter("*"))
async def arbitrage_menu_handler_command(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await message.answer(text=texts.commands.arbitrage.choose_arbitrage_type,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_arbitrage_menu_keyboard(texts=texts))


@arbitrage_menu_router.callback_query(F.data == "arbitrage", StateFilter("*"))
async def arbitrage_menu_handler_callback(call: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                                  disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await call.message.edit_text(text=texts.commands.arbitrage.choose_arbitrage_type,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_arbitrage_menu_keyboard(texts=texts))
