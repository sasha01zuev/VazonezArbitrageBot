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
                              get_settings_margin_hedging_keyboard, get_settings_loan_hedging_keyboard)
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "hedging_types"), StateFilter("*"))
async def select_hedging_type(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(texts.commands.settings.hedging_types.current_hedging_types,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_hedging_types_keyboard(texts=texts)
                                     )


@router.callback_query(SetHedgingTypesCallbackFactory.filter(F.hedging_type == "futures_hedging"), StateFilter("*"))
async def futures_hedging(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    hedging_futures = user_settings['hedging_futures']

    await callback.message.edit_text(texts.commands.settings.hedging_types.set_futures_hedging,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_futures_hedging_keyboard(texts=texts,
                                                                                        futures_hedging=hedging_futures)
                                     )


@router.callback_query(SetHedgingTypesCallbackFactory.filter(F.hedging_type == "margin_hedging"), StateFilter("*"))
async def margin_hedging(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    hedging_margin = user_settings['hedging_margin']

    await callback.message.edit_text(texts.commands.settings.hedging_types.set_margin_hedging,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_margin_hedging_keyboard(texts=texts,
                                                                                       margin_hedging=hedging_margin)
                                     )


@router.callback_query(SetHedgingTypesCallbackFactory.filter(F.hedging_type == "loan_hedging"), StateFilter("*"))
async def loan_hedging(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    hedging_loan = user_settings['hedging_loan']

    await callback.message.edit_text(texts.commands.settings.hedging_types.set_loan_hedging,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_loan_hedging_keyboard(texts=texts,
                                                                                     loan_hedging=hedging_loan)
                                     )


@router.callback_query(SetFuturesHedgingCallbackFactory.filter(), StateFilter("*"))
async def set_futures_hedging_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                    db: Database,
                                    callback_data: SetFuturesHedgingCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    hedging_value = callback_data.hedging_value
    hedging_type = "hedging_futures"

    try:

        await callback.message.edit_text(texts.commands.settings.hedging_types.current_hedging_types,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_futures_hedging_keyboard(texts=texts,
                                                                                            futures_hedging=hedging_value)
                                         )

        await db.set_user_inter_exchange_hedging(user_id=user_id, hedging_value=hedging_value,
                                                 hedging_type=hedging_type)

        await callback.answer(cache_time=2, text=texts.callback.successfully_changed)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)


@router.callback_query(SetMarginHedgingCallbackFactory.filter(), StateFilter("*"))
async def set_margin_hedging_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                   db: Database,
                                   callback_data: SetMarginHedgingCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    hedging_value = callback_data.hedging_value
    hedging_type = "hedging_margin"

    try:

        await callback.message.edit_text(texts.commands.settings.hedging_types.current_hedging_types,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_margin_hedging_keyboard(texts=texts,
                                                                                           margin_hedging=hedging_value)
                                         )

        await db.set_user_inter_exchange_hedging(user_id=user_id, hedging_value=hedging_value,
                                                 hedging_type=hedging_type)

        await callback.answer(cache_time=2, text=texts.callback.successfully_changed)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)


@router.callback_query(SetLoanHedgingCallbackFactory.filter(), StateFilter("*"))
async def set_loan_hedging_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                 db: Database,
                                 callback_data: SetLoanHedgingCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    hedging_value = callback_data.hedging_value
    hedging_type = "hedging_loan"

    try:

        await callback.message.edit_text(texts.commands.settings.hedging_types.current_hedging_types,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_loan_hedging_keyboard(texts=texts,
                                                                                         loan_hedging=hedging_value)
                                         )

        await db.set_user_inter_exchange_hedging(user_id=user_id, hedging_value=hedging_value,
                                                 hedging_type=hedging_type)

        await callback.answer(cache_time=2, text=texts.callback.successfully_changed)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)
