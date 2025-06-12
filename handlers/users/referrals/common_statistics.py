import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, ReferralsCallbackFactory, get_referral_statistics_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(ReferralsCallbackFactory.filter(F.item == "statistics"), StateFilter("*"))
async def referrals_statistics(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    await callback.answer(cache_time=1)

    logging.debug(f"Пользователь {user_id} запросил статистику рефералов")

    referrals_info = await db.get_user_referrals_info(user_id=user_id)
    referrals_quantity = referrals_info.get("referrals_quantity", 0)
    paid_subscriptions_quantity = referrals_info.get("paid_subscriptions_quantity", 0)
    balance = round(referrals_info.get("balance", 0), 2)
    total_earned = round(referrals_info.get("total_earned", 0), 2)

    await callback.message.edit_text(text=texts.commands.referrals.common_statistics.format(
        referrals_count=referrals_quantity, paid_subscriptions_quantity=paid_subscriptions_quantity,
        referral_balance=balance, total_earned=total_earned),
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_referral_statistics_keyboard(texts=texts)
    )
