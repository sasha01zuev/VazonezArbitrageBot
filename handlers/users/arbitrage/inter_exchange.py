from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_arbitrage_menu_keyboard, ArbitrageMenuCallbackFactory, get_back_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(ArbitrageMenuCallbackFactory.filter(F.arbitrage_type == "inter_exchange"),
                                      StateFilter("*"))
async def arbitrage_inter_exchange(call: Message, db: Database, texts: TextProxy, state: FSMContext):
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

    inter_exchange_subscription_status = texts.commands.arbitrage.inter_exchange.no_subscription

    if inter_exchange_subscription:
        delta = inter_exchange_subscription - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        inter_exchange_subscription_status = (f"🟢 {days}{texts.commands.arbitrage.day} "
                                              f"{hours}{texts.commands.arbitrage.hour} "
                                              f"{minutes}{texts.commands.arbitrage.minute} "
                                              f"{texts.commands.arbitrage.remain}")

        await call.message.edit_text(text=str(texts.commands.arbitrage.inter_exchange.active_subscription).format(
            subscription_status=inter_exchange_subscription_status),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_back_keyboard(texts=texts, callback_data="arbitrage"))
    else:
        await call.message.edit_text(text=texts.commands.arbitrage.inter_exchange.no_subscription,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_back_keyboard(texts=texts, callback_data="arbitrage"))
