import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory,  get_settings_notification_keyboard,
                              SetNotificationCallbackFactory)
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "notification"), StateFilter("*"))
async def set_notification(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    notification = user_settings['notification']
    await callback.message.edit_text(texts.commands.settings.notification.current_notification,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_notification_keyboard(texts=texts,
                                                                                     notification=notification)
                                     )


@router.callback_query(SetNotificationCallbackFactory.filter(), StateFilter("*"))
async def set_notification_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                            callback_data: SetNotificationCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    notification = False if callback_data.notification else True

    try:
        await callback.message.edit_text(texts.commands.settings.notification.current_notification,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_notification_keyboard(texts=texts,
                                                                                         notification=notification)
                                         )

        await db.set_user_inter_exchange_notification(user_id=user_id, notification=notification)

        await callback.answer(cache_time=2, text=texts.callback.notification.notification_enabled if notification else
        texts.callback.notification.notification_disabled)

    except TelegramBadRequest:
        await callback.answer(cache_time=2, text=texts.callback.no_changes)