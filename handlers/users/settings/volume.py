import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, get_settings_volume_keyboard, SetVolumeCallbackFactory, \
    get_back_keyboard
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import SetVolumeGroup

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "volume"), StateFilter("*"))
async def set_volume(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetVolumeGroup.SetMaxVolume]:
            logging.debug(f"Пользователь {callback.from_user.id} отменил настройку объёма")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")
    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        volume = user_settings['volume']
        await callback.message.edit_text(text=texts.commands.settings.volume.current_volume.format(
            volume=volume),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_volume_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetVolumeCallbackFactory.filter(F.volume_type == "volume"), StateFilter("*"))
async def set_volume_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(texts.commands.settings.volume.set_volume,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:volume"
                                                                    ))
    await state.set_state(SetVolumeGroup.SetMaxVolume)


@router.message(SetVolumeGroup.SetMaxVolume, StateFilter("*"))
async def set_max_volume(message: Message, state: FSMContext, texts: TextProxy, db: Database):
    user_id = message.from_user.id

    try:
        volume = message.text

        if ',' in volume or '.' in volume:
            volume = volume.replace(',', '')

        volume = int(volume)

        if volume <= 0:
            await message.answer(texts.commands.settings.volume.errors.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:volume"
                                                                ))
        elif volume >= 1_000_000:
            await message.answer(texts.commands.settings.volume.errors.greater_than_1000000,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:volume"
                                                                ))
        else:
            await db.set_user_inter_exchange_volume(user_id=user_id, volume=volume)
            await message.answer(texts.commands.settings.volume.success.volume.format(volume=volume),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:volume"
                                                                ))
            await state.clear()
    except ValueError:
        await message.answer(texts.commands.settings.volume.errors.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts,
                                                            callback_data="settings:volume"
                                                            ))
