import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, get_settings_spread_keyboard, SetSpreadCallbackFactory, get_back_keyboard, \
    get_settings_profit_keyboard, SetProfitCallbackFactory
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetProfitGroup

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "profit"), StateFilter("*"))
async def set_profit(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetProfitGroup.SetMinProfit]:
            logging.debug(f"Пользователь {callback.from_user.id} отменил настройку профита")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        profit = round(float(user_settings['profit']), 1)
        await callback.message.edit_text(text=texts.commands.settings.profit.current_profit.format(
            profit=profit),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_profit_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetProfitCallbackFactory.filter(F.profit_type == "profit"), StateFilter("*"))
async def set_profit_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(texts.commands.settings.profit.set_profit,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:profit"
                                                                    ))
    await state.set_state(SetProfitGroup.SetMinProfit)


@router.message(SetProfitGroup.SetMinProfit)
async def set_min_profit(message: Message, state: FSMContext, texts: TextProxy, db: Database):
    user_id = message.from_user.id

    try:
        profit = message.text

        if ',' in profit:
            profit = profit.replace(',', '.')
        profit = round(float(profit), 1)

        if profit <= 0:
            await message.answer(texts.commands.settings.profit.errors.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:profit"
                                                                ))
        elif profit >= 50_000:
            await message.answer(texts.commands.settings.profit.errors.greater_than_50000,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:profit"
                                                                ))
        else:
            await db.set_user_inter_exchange_profit(user_id=user_id, profit=profit)
            await message.answer(texts.commands.settings.profit.success.profit.format(profit=profit),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:profit"
                                                                ))
            await state.clear()
    except ValueError:
        await message.answer(texts.commands.settings.profit.errors.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts,callback_data="settings:profit")
                             )
