import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, ReferralsCallbackFactory, get_referral_statistics_keyboard, \
    ReferralsStatisticsCallbackFactory, get_back_keyboard, get_confirm_withdraw_keyboard, \
    ReferralsConfirmWithdrawCallbackFactory, get_subscriptions_for_convert_keyboard, \
    ReferralsConvertToSubscriptionCallbackFactory
from services.database.postgresql import Database
from states import SetReferralWithdrawGroup
from utils.i18n import TextProxy
from config.config import MAIN_ADMIN, SUBSCRIPTION_PRICE

router = Router()


@router.callback_query(ReferralsStatisticsCallbackFactory.filter(F.action == "convert_to_subscription"),
                       StateFilter("*"))
async def referrals_convert_to_subscription(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                            db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    logging.debug(f"Пользователь {user_id} нажал кнопку конвертации реферального баланса в подписку")

    referrals_info = await db.get_user_referrals_info(user_id=user_id)
    paid_subscriptions_quantity = referrals_info.get("paid_subscriptions_quantity", 0)
    balance = round(referrals_info.get("balance", 0), 2)

    one_week_price = SUBSCRIPTION_PRICE['inter_exchange']['one_week']
    one_month_price = SUBSCRIPTION_PRICE['inter_exchange']['one_month']
    three_month_price = SUBSCRIPTION_PRICE['inter_exchange']['three_month']
    lifetime_price = SUBSCRIPTION_PRICE['inter_exchange']['lifetime']

    if balance < one_week_price:
        await callback.message.edit_text(
            text=texts.commands.referrals.convert_to_subscription.errors.insufficient_balance.format(
                balance=balance, one_week_price=one_week_price, one_month_price=one_month_price,
                three_month_price=three_month_price, lifetime_price=lifetime_price
            ),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_back_keyboard(texts=texts,
                                           callback_data="referrals:statistics")
        )
        return
    else:
        logging.info(f"Пользователь {user_id} инициировал конвертацию реферального баланса в подписку")

        await callback.message.edit_text(text=texts.commands.referrals.convert_to_subscription.set_exchanges.format(
            balance=balance),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_subscriptions_for_convert_keyboard(
                texts=texts, subscriptions=SUBSCRIPTION_PRICE['inter_exchange'],
                balance=balance)
        )


@router.callback_query(ReferralsConvertToSubscriptionCallbackFactory.filter(), StateFilter("*"))
async def referrals_selected_type_subscription_to_convert(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                                          bot: Bot,
                                                          db: Database,
                                                          callback_data: ReferralsConvertToSubscriptionCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    await callback.answer(cache_time=1)

    user_id = callback.from_user.id
    subscription_type = callback_data.time

    logging.debug(f"Пользователь {user_id} выбрал тип подписки для конвертации: {subscription_type}")

    inter_exchange_subscriptions = SUBSCRIPTION_PRICE['inter_exchange']

    for subscription_time, price in inter_exchange_subscriptions.items():
        if subscription_time == subscription_type:
            selected_price = price
            logging.info(f"Пользователь {user_id} выбрал подписку {subscription_time} с ценой {selected_price}")

            await db.subtract_from_user_referral_balance(user_id=user_id, amount=selected_price)
            user_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
            logging.debug(f"Пользователь {user_id} имеет подписку: {user_subscription}")

            subscription_time = "1 week" if subscription_time == "one_week" else \
                "1 month" if subscription_time == "one_month" else \
                "3 month" if subscription_time == "three_month" else \
                "999 year" if subscription_time == "lifetime" else None
            if user_subscription:
                logging.info(f"Пользователь {user_id} уже имеет подписку, обновляем её")
                await db.add_user_subscription(user_id=user_id, subscription_type="inter_exchange",
                                               subscription_time=subscription_time)
            else:
                logging.info(f"Пользователь {user_id} не имеет подписки, создаем новую")
                await db.add_user_subscription(user_id=user_id, subscription_type="inter_exchange",
                                               subscription_time=subscription_time)

            referrals_info = await db.get_user_referrals_info(user_id=user_id)
            balance = round(referrals_info.get("balance", 0), 2)

            await callback.message.edit_text(
                text=texts.commands.referrals.convert_to_subscription.success.format(
                    balance=balance),
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts, callback_data="referrals:statistics")
            )

            # Notify admin about the subscription conversion
            await bot.send_message(MAIN_ADMIN, text=f"<b>Пользователь {user_id} конвертировал реферальный баланс в "
                                                    f"подписку {subscription_time} на сумму {selected_price}.</b>",
                                   disable_web_page_preview=True, parse_mode="HTML")

            break
