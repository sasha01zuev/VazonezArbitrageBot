import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SettingsCallbackFactory, get_back_keyboard, get_settings_withdraw_fee_keyboard,
                              SetWithdrawFeeCallbackFactory)
from services.database.postgresql import Database
from utils.i18n import TextProxy
from states import  SetWithdrawFeeGroup

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "withdraw_fee"), StateFilter("*"))
async def set_withdraw_fee(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")

        if await state.get_state() in [SetWithdrawFeeGroup.SetMaxWithdrawFee]:
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
        withdraw_fee = user_settings['withdraw_fee']

        await callback.message.edit_text(text=texts.commands.settings.withdraw_fee.current_withdraw_fee.format(
            withdraw_fee=withdraw_fee),
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_withdraw_fee_keyboard(texts=texts)
        )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(SetWithdrawFeeCallbackFactory.filter(F.withdraw_fee_type == "withdraw_fee"), StateFilter("*"))
async def set_withdraw_fee_value(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    await callback.message.edit_text(texts.commands.settings.withdraw_fee.set_withdraw_fee,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_back_keyboard(texts=texts,
                                                                    callback_data="settings:withdraw_fee"
                                                                    ))
    await state.set_state(SetWithdrawFeeGroup.SetMaxWithdrawFee)


@router.message(SetWithdrawFeeGroup.SetMaxWithdrawFee, StateFilter("*"))
async def set_max_withdraw_fee(message: Message, state: FSMContext, texts: TextProxy, db: Database):
    user_id = message.from_user.id

    try:
        withdraw_fee = message.text

        if ',' in withdraw_fee:
            withdraw_fee = withdraw_fee.replace(',', '.')

        withdraw_fee = round(float(withdraw_fee), 1)

        if withdraw_fee <= 0:
            await message.answer(texts.commands.settings.withdraw_fee.errors.less_than_0,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:withdraw_fee"
                                                                ))
        elif withdraw_fee >= 100_000:
            await message.answer(texts.commands.settings.withdraw_fee.errors.greater_than_100000,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:withdraw_fee"
                                                                ))
        else:
            await db.set_user_inter_exchange_withdraw_fee(user_id=user_id, withdraw_fee=withdraw_fee)
            await message.answer(texts.commands.settings.withdraw_fee.success.withdraw_fee.format(withdraw_fee=withdraw_fee),
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_back_keyboard(texts=texts,
                                                                callback_data="settings:withdraw_fee"
                                                                ))
            await state.clear()
    except ValueError:
        await message.answer(texts.commands.settings.withdraw_fee.errors.not_a_number,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_back_keyboard(texts=texts,
                                                            callback_data="settings:withdraw_fee"
                                                            ))
