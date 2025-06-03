import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_language_keyboard, \
    get_settings_contracts_keyboard, SetContractsCallbackFactory
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "contracts"), StateFilter("*"))
async def set_contracts(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    contracts = user_settings['contracts']
    await callback.message.edit_text(texts.commands.settings.contracts.set_contracts,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_contracts_keyboard(texts=texts, contracts=contracts)
                                     )


@router.callback_query(SetContractsCallbackFactory.filter(), StateFilter("*"))
async def set_contracts_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                            callback_data: SetContractsCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    contracts = callback_data.contracts_type

    try:
        await callback.message.edit_text(texts.commands.settings.contracts.set_contracts,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_contracts_keyboard(texts=texts, contracts=contracts)
                                         )
        await db.set_user_inter_exchange_contracts(user_id=user_id, contracts=contracts)
        await callback.answer(cache_time=2, text=texts.callback.successfully_changed)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)