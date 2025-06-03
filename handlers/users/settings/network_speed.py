import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, get_settings_volume_keyboard, SetVolumeCallbackFactory, \
    get_back_keyboard, get_settings_network_speed_keyboard, SetNetworkSpeedCallbackFactory
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetVolumeGroup
router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "network_speed"), StateFilter("*"))
async def set_network_speed(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        network_speed = user_settings['network_speed']
        show_undefined_networks = user_settings['show_undefined_networks']

        await callback.message.edit_text(text=texts.commands.settings.network_speed.set_network_speed,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_network_speed_keyboard(texts=texts, network_speed=network_speed,
                                                     show_undefined_networks=show_undefined_networks)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetNetworkSpeedCallbackFactory.filter(F.is_show_undefined_networks_chosen == True), StateFilter("*"))
async def set_network_speed_show_undefined_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                            callback_data: SetNetworkSpeedCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    if inter_exchange_subscription:
        await callback.answer(cache_time=2, text=texts.callback.network_speed)
        show_undefined_networks = False if callback_data.show_undefined_networks else True
        network_speed = callback_data.network_speed

        await db.set_user_inter_exchange_show_undefined_networks(user_id=user_id,
                                                                 show_undefined_networks=show_undefined_networks)
        await callback.message.edit_text(text=texts.commands.settings.network_speed.set_network_speed,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_network_speed_keyboard(texts=texts, network_speed=network_speed,
                                                     show_undefined_networks=show_undefined_networks)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetNetworkSpeedCallbackFactory.filter(F.is_show_undefined_networks_chosen == False), StateFilter("*"))
async def set_network_speed_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                            callback_data: SetNetworkSpeedCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    if inter_exchange_subscription:
        try:
            show_undefined_networks = callback_data.show_undefined_networks
            network_speed = callback_data.network_speed

            await db.set_user_inter_exchange_network_speed(user_id=user_id, network_speed=network_speed)
            await callback.message.edit_text(text=texts.commands.settings.network_speed.set_network_speed,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_network_speed_keyboard(texts=texts, network_speed=network_speed,
                                                         show_undefined_networks=show_undefined_networks)
            )
            await callback.answer(cache_time=2, text=texts.callback.network_speed)
        except TelegramBadRequest:
            await callback.answer(cache_time=2, text=texts.callback.no_changes)
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)