from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
import logging

from keyboards.inline import get_arbitrage_menu_keyboard, get_support_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from config.config import SUBSCRIPTION_PRICE, WALLETS_ADDRESS

subscriptions_router = Router()


@subscriptions_router.message(Command("subscriptions"), StateFilter("*"))
async def subscriptions_handler_command(message: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {message.from_user.id}")
        await message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await message.answer(text=texts.commands.subscriptions.inter_exchange.price_list.format(
        one_week_price=SUBSCRIPTION_PRICE['inter_exchange']['one_week'],
        one_month_price=SUBSCRIPTION_PRICE['inter_exchange']['one_month'],
        three_month_price=SUBSCRIPTION_PRICE['inter_exchange']['three_month'],
        lifetime_price=SUBSCRIPTION_PRICE['inter_exchange']['lifetime'],
        bep20_address=WALLETS_ADDRESS['BEP20'],
        trc20_address=WALLETS_ADDRESS['TRC20']
    ), disable_web_page_preview=True, parse_mode="HTML", reply_markup=get_support_keyboard(texts=texts))


@subscriptions_router.callback_query(F.data == "subscriptions", StateFilter("*"))
async def subscriptions_handler_callback(call: Message, db: Database, texts: TextProxy, state: FSMContext):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {call.from_user.id}")
        await call.message.answer(text=texts.commands.state.canceled_state,
                                  disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await call.message.edit_text(text=texts.commands.subscriptions.inter_exchange.price_list.format(
        one_week_price=SUBSCRIPTION_PRICE['inter_exchange']['one_week'],
        one_month_price=SUBSCRIPTION_PRICE['inter_exchange']['one_month'],
        three_month_price=SUBSCRIPTION_PRICE['inter_exchange']['three_month'],
        lifetime_price=SUBSCRIPTION_PRICE['inter_exchange']['lifetime'],
        bep20_address=WALLETS_ADDRESS['BEP20'],
        trc20_address=WALLETS_ADDRESS['TRC20']
    ), disable_web_page_preview=True, parse_mode="HTML", reply_markup=get_support_keyboard(texts=texts))
