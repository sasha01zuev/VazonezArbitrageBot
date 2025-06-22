import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config.config import SUBSCRIPTION_PRICE, WALLETS_ADDRESS, MAIN_ADMIN
from handlers.users.menu import menu_handler_callback
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, ReferralsCallbackFactory, get_referral_statistics_keyboard, \
    SubscriptionsArbitrageTypeCallbackFactory, get_support_keyboard, subscriptions_type_keyboard, \
    SubscriptionsTypeCallbackFactory, subscriptions_pay_keyboard, SubscriptionsPayCallbackFactory, \
    subscriptions_monitoring_keyboard, SubscriptionsCancelMonitoringCallbackFactory
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SubscriptionsArbitrageTypeCallbackFactory.filter(F.arbitrage_type == "inter_exchange"),
                       StateFilter("*"))
async def subscriptions_inter_exchange(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                       bot: Bot, db: Database,
                                       callback_data: SubscriptionsArbitrageTypeCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id
    await callback.answer(cache_time=1)

    users_wallets_in_monitoring = await db.get_user_wallets_in_monitoring(user_id)

    if users_wallets_in_monitoring:
        available_wallet_time = await db.get_user_available_time_wallet(user_id)
        available_minutes, available_seconds = available_wallet_time

        usdt_trc20_address = users_wallets_in_monitoring["usdt_trc20_address"]
        usdt_bep20_address = users_wallets_in_monitoring["usdt_bep20_address"]
        subscription_price = users_wallets_in_monitoring["subscription_price"]
        subscription_type = users_wallets_in_monitoring["subscription_type"]
        arbitrage_type = users_wallets_in_monitoring["arbitrage_type"]
        arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" \
            else "Unknown"

        subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
            texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                    texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

        await callback.message.edit_text(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )
    else:
        inter_exchange_subscription = await db.get_user_subscription(user_id=user_id,
                                                                     subscription_type="inter_exchange")

        if inter_exchange_subscription:
            current_subscription_message = texts.commands.subscriptions.inter_exchange.current_subscription_message
        else:
            current_subscription_message = ""

        await callback.message.edit_text(text=texts.commands.subscriptions.inter_exchange.price_list.format(
            one_week_price=SUBSCRIPTION_PRICE['inter_exchange']['one_week'],
            one_month_price=SUBSCRIPTION_PRICE['inter_exchange']['one_month'],
            three_month_price=SUBSCRIPTION_PRICE['inter_exchange']['three_month'],
            lifetime_price=SUBSCRIPTION_PRICE['inter_exchange']['lifetime'],
            bep20_address=WALLETS_ADDRESS['BEP20'],
            trc20_address=WALLETS_ADDRESS['TRC20'],
            current_subscription_message=current_subscription_message
        ), disable_web_page_preview=True, parse_mode="HTML", reply_markup=subscriptions_type_keyboard(texts=texts))


@router.callback_query(SubscriptionsTypeCallbackFactory.filter(F.payment_type == "auto"), StateFilter("*"))
async def subscriptions_inter_exchange(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                       bot: Bot, db: Database, callback_data: SubscriptionsTypeCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    users_wallets_in_monitoring = await db.get_user_wallets_in_monitoring(user_id)

    if users_wallets_in_monitoring:
        available_wallet_time = await db.get_user_available_time_wallet(user_id)
        available_minutes, available_seconds = available_wallet_time

        usdt_trc20_address = users_wallets_in_monitoring["usdt_trc20_address"]
        usdt_bep20_address = users_wallets_in_monitoring["usdt_bep20_address"]
        subscription_price = users_wallets_in_monitoring["subscription_price"]
        subscription_type = users_wallets_in_monitoring["subscription_type"]
        arbitrage_type = users_wallets_in_monitoring["arbitrage_type"]
        arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" \
            else "Unknown"

        subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
            texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                    texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

        await callback.message.edit_text(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )
    else:
        subscription_type_callback = callback_data.subscription_type

        subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type_callback == 'one_week' else \
            texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type_callback == 'one_month' else \
                texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type_callback == 'three_month' else \
                    texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

        await callback.message.edit_text(text=texts.commands.subscriptions.inter_exchange.confirm_payment.format(
            arbitrage_type=texts.keyboard.arbitrage.buttons.inter_exchange,
            subscription_type=subscription_type,
            price=SUBSCRIPTION_PRICE['inter_exchange'][subscription_type_callback],
        ), disable_web_page_preview=True, parse_mode="HTML", reply_markup=subscriptions_pay_keyboard(
            texts=texts, subscription_type=subscription_type_callback, arbitrage_type="inter_exchange"))


@router.callback_query(SubscriptionsPayCallbackFactory.filter(), StateFilter("*"))
async def subscriptions_go_to_payment(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                      bot: Bot, db: Database, callback_data: SubscriptionsPayCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    users_wallets_in_monitoring = await db.get_user_wallets_in_monitoring(user_id)

    if users_wallets_in_monitoring:
        available_wallet_time = await db.get_user_available_time_wallet(user_id)
        available_minutes, available_seconds = available_wallet_time

        usdt_trc20_address = users_wallets_in_monitoring["usdt_trc20_address"]
        usdt_bep20_address = users_wallets_in_monitoring["usdt_bep20_address"]
        subscription_price = users_wallets_in_monitoring["subscription_price"]
        subscription_type = users_wallets_in_monitoring["subscription_type"]
        arbitrage_type = users_wallets_in_monitoring["arbitrage_type"]
        arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" \
            else "Unknown"

        subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
            texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                    texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

        await callback.message.edit_text(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )
    else:
        subscription_type_callback = callback_data.subscription_type
        arbitrage_type = callback_data.arbitrage_type
        logging.debug(
            f"Пользователь {user_id} выбрал подписку {subscription_type_callback} для типа арбитража {arbitrage_type}")
        all_monitoring_wallets = await db.get_all_monitoring_wallets()

        if len(all_monitoring_wallets) > 100:
            delay = await db.get_next_available_wallet_delay()
            minutes, seconds = delay

            await callback.answer(cache_time=1,
                                  text=texts.callback.subscriptions.too_many_wallets.format(
                                      minutes=minutes, seconds=seconds
                                  ), show_alert=True)
            return

        await callback.answer(cache_time=1)

        await db.add_user_wallets_to_monitoring(user_id, time="20 minute",
                                                subscription_price=SUBSCRIPTION_PRICE[arbitrage_type][
                                                    subscription_type_callback],
                                                subscription_type=subscription_type_callback,
                                                arbitrage_type=arbitrage_type)

        reminder_thresholds = [15, 10, 5, 3, 1, 0]
        time_reminder = {}
        for threshold in reminder_thresholds:
            field_name = f"{threshold}_minutes"
            time_reminder[field_name] = False
        time_reminder["expired"] = False

        await db.update_time_reminder(user_id, time_reminder)

        users_wallets_in_monitoring = await db.get_user_wallets_in_monitoring(user_id)

        usdt_trc20_address = users_wallets_in_monitoring["usdt_trc20_address"]
        usdt_bep20_address = users_wallets_in_monitoring["usdt_bep20_address"]
        usdt_trc20_key = users_wallets_in_monitoring["usdt_trc20_key"]
        usdt_bep20_key = users_wallets_in_monitoring["usdt_bep20_key"]
        subscription_price = users_wallets_in_monitoring["subscription_price"]

        available_wallet_time = await db.get_user_available_time_wallet(user_id)
        available_minutes, available_seconds = available_wallet_time

        subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type_callback == 'one_week' else \
            texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type_callback == 'one_month' else \
                texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type_callback == 'three_month' else \
                    texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

        arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" else "Unknown"

        await callback.message.edit_text(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )

        await bot.send_message(chat_id=MAIN_ADMIN,
                               text=f"Пользователь <code>{user_id}</code> <code>{callback.from_user.first_name}</code> "
                                    f"@{callback.from_user.username}\n"
                                    f"Нажал ОПЛАТИТЬ ПОДПИСКУ <code>{subscription_type_callback}</code> для типа арбитража <code>{arbitrage_type}</code>.\n\n"
                                    f"Адреса USDT: \n\n"
                                    f"<b>TRC20:</b> <code>{usdt_trc20_address}</code>\n"
                                    f"<b>Ключ TRC20:</b> <code>{usdt_trc20_key}</code>\n\n"
                                    f"<b>BEP20:</b> <code>{usdt_bep20_address}</code>\n"
                                    f"<b>Ключ BEP20:</b> <code>{usdt_bep20_key}</code>\n\n"
                                    f"Цена подписки: <code>{subscription_price}$</code>\n",
                               parse_mode="HTML", disable_web_page_preview=True)


@router.callback_query(SubscriptionsCancelMonitoringCallbackFactory.filter(F.action == "cancel_monitoring"),
                       StateFilter("*"))
async def subscriptions_cancel_monitoring(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                          bot: Bot, db: Database, callback_data: SubscriptionsPayCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    user_id = callback.from_user.id
    await db.cancel_user_wallets_in_monitoring(user_id)
    time_reminder = {
        "15_minutes": False,
        "10_minutes": False,
        "5_minutes": False,
        "3_minutes": False,
        "1_minutes": False,
        "0_minutes": False,
        "expired": True
    }
    payment_status = {
        "confirmed": False,
        "insufficient": False,
        "pending_confirmation": False
    }

    await db.update_time_reminder(user_id, time_reminder)
    await db.update_payment_status(user_id, payment_status)

    await callback.answer(cache_time=1,
                          text=texts.callback.subscriptions.cancel_monitoring, show_alert=True)

    await menu_handler_callback(call=callback, db=db, texts=texts, state=state)
