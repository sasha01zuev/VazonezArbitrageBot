from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_arbitrage_menu_keyboard, get_support_keyboard, \
    subscriptions_arbitrage_type_keyboard_keyboard, SubscriptionsTypeCallbackFactory, subscriptions_monitoring_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from config.config import SUBSCRIPTION_PRICE, WALLETS_ADDRESS

subscriptions_menu_router = Router()


@subscriptions_menu_router.message(Command("subscriptions"), StateFilter("*"))
async def subscriptions_handler_command(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    user_id = message.from_user.id
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

        await message.answer(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )
    else:
        await message.answer(text=texts.commands.subscriptions.choose_arbitrage_type,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=subscriptions_arbitrage_type_keyboard_keyboard(texts=texts))


@subscriptions_menu_router.callback_query(F.data == "subscriptions", StateFilter("*"))
async def subscriptions_handler_callback(call: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                                  disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    await call.answer(cache_time=1)
    user_id = call.from_user.id

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

        await call.message.edit_text(
            text=texts.commands.subscriptions.inter_exchange.monitoring_payment.format(
                minutes=available_minutes, seconds=available_seconds,
                arbitrage_type=arbitrage_type_message,
                subscription_type=subscription_type, price=subscription_price,
                usdt_trc20_address=usdt_trc20_address, usdt_bep20_address=usdt_bep20_address),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=subscriptions_monitoring_keyboard(texts=texts)
        )
    else:
        await call.message.edit_text(text=texts.commands.subscriptions.choose_arbitrage_type,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=subscriptions_arbitrage_type_keyboard_keyboard(texts=texts))


@subscriptions_menu_router.callback_query(SubscriptionsTypeCallbackFactory.filter(F.payment_type == "manual"),
                                          StateFilter("*"))
async def subscriptions_inter_exchange(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                       bot: Bot, db: Database, callback_data: SubscriptionsTypeCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()
    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.subscriptions.inter_exchange.price_list_legacy.format(
        one_week_price=SUBSCRIPTION_PRICE['inter_exchange']['one_week'],
        one_month_price=SUBSCRIPTION_PRICE['inter_exchange']['one_month'],
        three_month_price=SUBSCRIPTION_PRICE['inter_exchange']['three_month'],
        lifetime_price=SUBSCRIPTION_PRICE['inter_exchange']['lifetime'],
        bep20_address=WALLETS_ADDRESS['BEP20'],
        trc20_address=WALLETS_ADDRESS['TRC20']
    ), disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_support_keyboard(texts=texts,
                                          callback_data="subscriptions_arbitrage:inter_exchange"))
