from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_main_keyboard, get_settings_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from .menu import menu_router
settings_menu_router = Router()


@settings_menu_router.message(Command("settings"), StateFilter("*"))
async def settings_handler(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    user_id = message.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    logging.debug(f"Межбиржевая подписка пользователя {user_id}: {inter_exchange_subscription}")

    now = datetime.now(timezone.utc)

    inter_exchange_subscription_status = f"❌ {texts.commands.settings.no_subscription}"

    if inter_exchange_subscription:
        delta = inter_exchange_subscription - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        inter_exchange_subscription_status = (f"🟢 {days}{texts.commands.settings.day} "
                                              f"{hours}{texts.commands.settings.hour} "
                                              f"{minutes}{texts.commands.settings.minute} "
                                              f"{texts.commands.settings.remain}")
    await message.answer(text=str(texts.commands.settings).format(user_id=user_id, subscription_status=inter_exchange_subscription_status),
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_settings_keyboard(texts=texts))


@settings_menu_router.callback_query(F.data == "settings", StateFilter("*"))
async def settings_handler(call: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await call.answer(cache_time=1)
    user_id = call.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    logging.debug(f"Межбиржевая подписка пользователя {user_id}: {inter_exchange_subscription}")

    now = datetime.now(timezone.utc)

    inter_exchange_subscription_status = f"❌ {texts.commands.settings.no_subscription}"

    if inter_exchange_subscription:
        delta = inter_exchange_subscription - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        inter_exchange_subscription_status = (f"🟢 {days}{texts.commands.settings.day} "
                                              f"{hours}{texts.commands.settings.hour} "
                                              f"{minutes}{texts.commands.settings.minute} "
                                              f"{texts.commands.settings.remain}")

    await call.message.edit_text(text=str(texts.commands.settings).format(user_id=user_id, subscription_status=inter_exchange_subscription_status),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_settings_keyboard(texts=texts))
