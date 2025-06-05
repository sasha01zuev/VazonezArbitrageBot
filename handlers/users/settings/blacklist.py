import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory, get_settings_hedging_types_keyboard,
                              SetHedgingTypesCallbackFactory, SetFuturesHedgingCallbackFactory,
                              SetMarginHedgingCallbackFactory, SetLoanHedgingCallbackFactory,
                              get_settings_futures_hedging_keyboard,
                              get_settings_margin_hedging_keyboard, get_settings_loan_hedging_keyboard,
                              get_settings_blacklist_types_keyboard)
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "blacklist_types"), StateFilter("*"))
async def select_blacklist_type(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(texts.commands.settings.blacklist_types.current_blacklist_types,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_blacklist_types_keyboard(texts=texts))
