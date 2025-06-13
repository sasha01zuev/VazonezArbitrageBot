import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory, get_settings_notification_keyboard,
                              SetNotificationCallbackFactory, get_settings_is_low_bids_keyboard,
                              SetIsLowBidsCallbackFactory)
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "is_low_bids"), StateFilter("*"))
async def set_is_low_bids(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")

    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        is_low_bids = user_settings['is_low_bids']
        await callback.message.edit_text(texts.commands.settings.is_low_bids.current_is_low_bids,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_is_low_bids_keyboard(texts=texts,
                                                                                        is_low_bids=is_low_bids)
                                         )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetIsLowBidsCallbackFactory.filter(), StateFilter("*"))
async def set_notification_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                                 callback_data: SetIsLowBidsCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    is_low_bids = callback_data.is_low_bids

    try:
        await callback.message.edit_text(texts.commands.settings.is_low_bids.current_is_low_bids,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_is_low_bids_keyboard(texts=texts,
                                                                                        is_low_bids=is_low_bids)
                                         )

        await db.set_user_inter_exchange_is_low_bids(user_id=user_id, is_low_bids=is_low_bids)

        await callback.answer(cache_time=2, text=texts.callback.successfully_changed)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)
