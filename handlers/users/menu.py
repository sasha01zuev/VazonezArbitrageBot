from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_main_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from services.wallets import BEP20Wallet, TRC20Wallet

menu_router = Router()


@menu_router.message(Command("menu"), StateFilter("*"))
async def menu_handler_message(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")

    await state.clear()

    await message.answer(text=texts.commands.menu,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_main_keyboard(texts=texts))


@menu_router.callback_query(F.data == "menu", StateFilter("*"))
async def menu_handler_callback(call: CallbackQuery, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                                  disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await call.answer(cache_time=1)
    await call.message.edit_text(
        text=texts.commands.menu,
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_main_keyboard(texts=texts))
