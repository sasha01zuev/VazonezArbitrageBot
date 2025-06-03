import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory, get_back_keyboard, get_settings_coin_volume_24h_keyboard,
                              SetCoinVolume24hCallbackFactory, get_settings_last_trade_time_keyboard,
                              SetLastTradeTimeCallbackFactory)
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetLastTradeTimeGroup

router = Router()


def format_seconds_to_hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}ч. {minutes}м. {secs}с."


def parse_hms_input_to_seconds(text: str) -> int:
    try:
        parts = list(map(int, text.strip().split()))
        while len(parts) < 3:
            parts.append(0)  # если ввели только 2 числа — добавим нули
        hours, minutes, seconds = parts[:3]
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    except Exception as e:
        raise ValueError("Неверный формат. Введите три числа через пробел: часы минуты секунды.")


@router.callback_query(SettingsCallbackFactory.filter(F.item == "last_trade_time"), StateFilter("*"))
async def set_last_trade_time(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetLastTradeTimeGroup.SetMinLastTradeTime,
                                       SetLastTradeTimeGroup.SetMaxLastTradeTime]:
            logging.debug(f"Пользователь {callback.from_user.id} отменил настройку спреда")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")

    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        min_last_trade_time = user_settings['min_last_trade_time']
        max_last_trade_time = user_settings['max_last_trade_time']

        await callback.message.edit_text(text=texts.commands.settings.last_trade_time.current_last_trade_time.format(
            min_last_trade_time=format_seconds_to_hms(min_last_trade_time),
            max_last_trade_time=format_seconds_to_hms(max_last_trade_time)),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_last_trade_time_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetLastTradeTimeCallbackFactory.filter(F.last_trade_time_type == "max_last_trade_time"),
                       StateFilter("*"))
async def set_max_last_trade_time(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.settings.last_trade_time.set_max_last_trade_time,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:last_trade_time"))
    await state.set_state(SetLastTradeTimeGroup.SetMaxLastTradeTime)


@router.message(SetLastTradeTimeGroup.SetMaxLastTradeTime)
async def set_max_last_trade_time_value(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        max_last_trade_time = parse_hms_input_to_seconds(message.text)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        min_last_trade_time = user_settings['min_last_trade_time']

        if max_last_trade_time < 0:
            await message.answer(text=texts.commands.settings.last_trade_time.errors.max_last_trade_time.negative_value,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:last_trade_time")
                                 )
            return
        if max_last_trade_time <= min_last_trade_time:
            await message.answer(text=texts.commands.settings.last_trade_time.errors.max_last_trade_time.less_than_min,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:last_trade_time")
                                 )
            return
        if max_last_trade_time > 1_000_000:
            await message.answer(
                text=texts.commands.settings.last_trade_time.errors.max_last_trade_time.greater_than_1000000,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts,
                                               callback_data="settings:last_trade_time")
                )
            return

    except ValueError:
        await message.answer(text=texts.commands.settings.last_trade_time.errors.max_last_trade_time.invalid_format,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts,
                                                            callback_data="settings:last_trade_time")
                             )
        return

    await db.set_user_inter_exchange_last_trade_time(user_id=user_id, last_trade_time=max_last_trade_time,
                                                     last_trade_time_type="max_last_trade_time")

    await message.answer(text=texts.commands.settings.last_trade_time.success.max_last_trade_time.format(
        max_last_trade_time=format_seconds_to_hms(max_last_trade_time)),
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_back_keyboard(texts=texts, callback_data="settings:last_trade_time"))

    await state.clear()


@router.callback_query(SetLastTradeTimeCallbackFactory.filter(F.last_trade_time_type == "min_last_trade_time"),
                       StateFilter("*"))
async def set_min_last_trade_time(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.settings.last_trade_time.set_min_last_trade_time,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:last_trade_time"))
    await state.set_state(SetLastTradeTimeGroup.SetMinLastTradeTime)


@router.message(SetLastTradeTimeGroup.SetMinLastTradeTime)
async def set_min_last_trade_time_value(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        min_last_trade_time = parse_hms_input_to_seconds(message.text)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        max_last_trade_time = user_settings['max_last_trade_time']

        if min_last_trade_time < 0:
            await message.answer(text=texts.commands.settings.last_trade_time.errors.min_last_trade_time.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:last_trade_time")
                                 )
            return
        if min_last_trade_time >= max_last_trade_time:
            await message.answer(
                text=texts.commands.settings.last_trade_time.errors.min_last_trade_time.greater_than_max,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts,
                                               callback_data="settings:last_trade_time")
                )
            return
        if min_last_trade_time > 1_000_000:
            await message.answer(
                text=texts.commands.settings.last_trade_time.errors.min_last_trade_time.greater_than_1000000,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts,
                                               callback_data="settings:last_trade_time")
                )
            return

    except ValueError:
        await message.answer(text=texts.commands.settings.last_trade_time.errors.min_last_trade_time.invalid_format,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts,
                                                            callback_data="settings:last_trade_time")
                             )
        return

    await db.set_user_inter_exchange_last_trade_time(user_id=user_id, last_trade_time=min_last_trade_time,
                                                     last_trade_time_type="min_last_trade_time")

    await message.answer(text=texts.commands.settings.last_trade_time.success.min_last_trade_time.format(
        min_last_trade_time=format_seconds_to_hms(min_last_trade_time)),
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_back_keyboard(texts=texts, callback_data="settings:last_trade_time"))

    await state.clear()
