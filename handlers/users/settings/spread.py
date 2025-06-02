import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, get_settings_spread_keyboard, SetSpreadCallbackFactory, get_back_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetSpreadGroup

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "spread"), StateFilter("*"))
async def set_spread(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetSpreadGroup.SetMinSpread, SetSpreadGroup.SetMaxSpread]:
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
        min_spread = round(float(user_settings['min_spread']), 1)
        max_spread = round(float(user_settings['max_spread']), 1)
        await callback.message.edit_text(text=texts.commands.settings.spread.current_spread.format(
            min_spread=min_spread, max_spread=max_spread),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_spread_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetSpreadCallbackFactory.filter(F.spread_type == "max_spread"), StateFilter("*"))
async def set_max_spread(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(text=texts.commands.settings.spread.set_max_spread,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:spread"
                                                                    )
                                     )
    await state.set_state(SetSpreadGroup.SetMaxSpread)


@router.message(SetSpreadGroup.SetMaxSpread)
async def set_max_spread_handler(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        max_spread = message.text

        if ',' in max_spread:
            max_spread = max_spread.replace(',', '.')
        max_spread = round(float(max_spread), 1)

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        min_spread = round(float(user_settings['min_spread']), 1)

        if max_spread <= min_spread:
            await message.answer(text=texts.commands.settings.spread.errors.max_spread.less_than_min,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread"))
        elif max_spread > 100:
            await message.answer(text=texts.commands.settings.spread.errors.max_spread.greater_than_100,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread"))
        else:
            await db.set_user_inter_exchange_spread(user_id=user_id, spread_type='max_spread', spread=max_spread)
            await message.answer(texts.commands.settings.spread.success.max_spread.format(max_spread=max_spread,
                                                                                          min_spread=min_spread),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread")
                                 )
            await state.clear()

    except ValueError:
        await message.answer(text=texts.commands.settings.spread.errors.max_spread.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML")


@router.callback_query(SetSpreadCallbackFactory.filter(F.spread_type == "min_spread"), StateFilter("*"))
async def set_min_spread(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)
    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    min_spread = round(float(user_settings['min_spread']), 1)
    max_spread = round(float(user_settings['max_spread']), 1)

    await callback.message.edit_text(text=texts.commands.settings.spread.set_min_spread,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:spread"
                                                                    )
                                     )
    await state.set_state(SetSpreadGroup.SetMinSpread)


@router.message(SetSpreadGroup.SetMinSpread)
async def set_min_spread_handler(message: Message, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    user_id = message.from_user.id

    try:
        min_spread = message.text

        if ',' in min_spread:
            min_spread = min_spread.replace(',', '.')
        min_spread = round(float(min_spread), 1)

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        max_spread = round(float(user_settings['max_spread']), 1)

        if min_spread >= max_spread:
            await message.answer(text=texts.commands.settings.spread.errors.min_spread.greater_than_max,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread"))
        elif min_spread < 0:
            await message.answer(text=texts.commands.settings.spread.errors.min_spread.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread"))
        else:
            await db.set_user_inter_exchange_spread(user_id=user_id, spread_type='min_spread', spread=min_spread)
            await message.answer(texts.commands.settings.spread.success.min_spread.format(min_spread=min_spread,
                                                                                          max_spread=max_spread),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts, callback_data="settings:spread")
                                 )
            await state.clear()

    except ValueError:
        await message.answer(text=texts.commands.settings.spread.errors.min_spread.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML")
