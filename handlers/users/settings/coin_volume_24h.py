import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory, get_back_keyboard, get_settings_coin_volume_24h_keyboard,
                              SetCoinVolume24hCallbackFactory)
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetCoinVolume24hGroup

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "coin_volume_24h"), StateFilter("*"))
async def set_coin_volume_24h(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetCoinVolume24hGroup.SetMinCoinVolume24h,
                                       SetCoinVolume24hGroup.SetMaxCoinVolume24h]:
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
        min_coin_volume_24h = user_settings['min_coin_24_volume']
        max_coin_volume_24h = user_settings['max_coin_24_volume']

        await callback.message.edit_text(text=texts.commands.settings.volume_24h.current_volume_24h.format(
            min_coin_volume_24h=min_coin_volume_24h, max_coin_volume_24h=max_coin_volume_24h),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_volume_24h_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetCoinVolume24hCallbackFactory.filter(F.coin_volume_24h_type == "max_coin_volume_24h"),
                       StateFilter("*"))
async def set_max_coin_volume_24h(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.settings.volume_24h.set_max_coin_volume_24h,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:coin_volume_24h"
                                                                    )
                                     )
    await state.set_state(SetCoinVolume24hGroup.SetMaxCoinVolume24h)


@router.message(SetCoinVolume24hGroup.SetMaxCoinVolume24h)
async def set_max_coin_volume_24h_value(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        max_coin_volume_24h = message.text

        if ',' in max_coin_volume_24h:
            max_coin_volume_24h = max_coin_volume_24h.replace(',', '.')

        max_coin_volume_24h = float(max_coin_volume_24h)
        max_coin_volume_24h = int(max_coin_volume_24h)

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        min_coin_volume_24h = user_settings['min_coin_24_volume']

        if max_coin_volume_24h <= min_coin_volume_24h:
            await message.answer(text=texts.commands.settings.volume_24h.errors.max_coin_volume_24h.less_than_min,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))
        elif max_coin_volume_24h > 100_000_000_000:
            await message.answer(text=texts.commands.settings.volume_24h.errors.max_coin_volume_24h.greater_than_100000000000,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))
        else:
            await db.set_user_inter_exchange_coin_volume_24h(user_id=user_id, coin_volume_24h_type='max_coin_24_volume',
                                                    coin_volume_24h=max_coin_volume_24h)
            await message.answer(texts.commands.settings.volume_24h.success.max_coin_volume_24h.format(
                max_coin_volume_24h=max_coin_volume_24h), disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))

            await state.clear()

    except ValueError:
        await message.answer(text=texts.commands.settings.volume_24h.errors.max_coin_volume_24h.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))


@router.callback_query(SetCoinVolume24hCallbackFactory.filter(F.coin_volume_24h_type == "min_coin_volume_24h"),
                       StateFilter("*"))
async def set_min_coin_volume_24h(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.settings.volume_24h.set_min_coin_volume_24h,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:coin_volume_24h"
                                                                    )
                                     )
    await state.set_state(SetCoinVolume24hGroup.SetMinCoinVolume24h)


@router.message(SetCoinVolume24hGroup.SetMinCoinVolume24h)
async def set_min_coin_volume_24h_value(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        min_coin_volume_24h = message.text

        if ',' in min_coin_volume_24h:
            min_coin_volume_24h = min_coin_volume_24h.replace(',', '.')

        min_coin_volume_24h = float(min_coin_volume_24h)
        min_coin_volume_24h = int(min_coin_volume_24h)

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        max_coin_volume_24h = user_settings['max_coin_24_volume']

        if min_coin_volume_24h >= max_coin_volume_24h:
            await message.answer(text=texts.commands.settings.volume_24h.errors.min_coin_volume_24h.greater_than_max,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))
        elif min_coin_volume_24h < 0:
            await message.answer(text=texts.commands.settings.volume_24h.errors.min_coin_volume_24h.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))
        else:
            await db.set_user_inter_exchange_coin_volume_24h(user_id=user_id, coin_volume_24h_type='min_coin_24_volume',
                                                    coin_volume_24h=min_coin_volume_24h)
            await message.answer(texts.commands.settings.volume_24h.success.min_coin_volume_24h.format(
                min_coin_volume_24h=min_coin_volume_24h), disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))

            await state.clear()

    except ValueError:
        await message.answer(text=texts.commands.settings.volume_24h.errors.min_coin_volume_24h.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts, callback_data="settings:coin_volume_24h"))


