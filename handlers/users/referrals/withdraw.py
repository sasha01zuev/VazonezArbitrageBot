import asyncio
import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory, ReferralsCallbackFactory, get_referral_statistics_keyboard, \
    ReferralsStatisticsCallbackFactory, get_back_keyboard, get_confirm_withdraw_keyboard, \
    ReferralsConfirmWithdrawCallbackFactory
from services.database.postgresql import Database
from states import SetReferralWithdrawGroup
from utils.i18n import TextProxy
from config.config import MAIN_ADMIN

router = Router()


@router.callback_query(ReferralsStatisticsCallbackFactory.filter(F.action == "withdraw"), StateFilter("*"))
async def referrals_withdraw_funds(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                   db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                                      disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    logging.debug(f"Пользователь {user_id} нажал кнопку вывода средств из реферальной программы")

    referrals_info = await db.get_user_referrals_info(user_id=user_id)
    paid_subscriptions_quantity = referrals_info.get("paid_subscriptions_quantity", 0)
    balance = referrals_info.get("balance", 0)

    if balance <= 0:
        await callback.answer(text=texts.callback.referrals.referrals_statistics.withdraw.errors.zero_balance,
                              show_alert=True)
        return
    elif balance < 5:
        await callback.answer(text=texts.callback.referrals.referrals_statistics.withdraw.errors.balance_less_than_5,
                              show_alert=True)
        return
    elif paid_subscriptions_quantity < 2:
        await callback.answer(
            text=texts.callback.referrals.referrals_statistics.withdraw.errors.paid_subscriptions_quantity_less_than_2,
            show_alert=True)
        return
    else:
        logging.info(f"Пользователь {user_id} инициировал вывод средств из реферальной программы")

        await callback.message.edit_text(text=texts.commands.referrals.withdraw.set_network,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_back_keyboard(texts=texts,
                                                                        callback_data="referrals:statistics")
                                         )
        await state.set_state(SetReferralWithdrawGroup.SetNetwork)
        await state.update_data(balance=balance)


@router.message(SetReferralWithdrawGroup.SetNetwork)
async def set_network_for_withdraw(message: Message, state: FSMContext, texts: TextProxy, db: Database):
    user_id = message.from_user.id
    network = message.text.strip().upper()

    logging.debug(f"Пользователь {user_id} ввел сеть для вывода средств: {network}")

    await state.update_data(network=network)

    await message.answer(text=texts.commands.referrals.withdraw.set_address,
                         disable_web_page_preview=True, parse_mode="HTML",
                         reply_markup=get_back_keyboard(texts=texts,
                                                        callback_data="referrals:statistics"
                                                        )
                         )
    await state.set_state(SetReferralWithdrawGroup.SetAddress)


@router.message(SetReferralWithdrawGroup.SetAddress)
async def set_address_for_withdraw(message: Message, state: FSMContext, texts: TextProxy, db: Database):
    user_id = message.from_user.id
    address = message.text.strip().upper()
    state_data = await state.get_data()
    network = state_data.get("network", "")
    balance = round(float(state_data.get("balance")), 2)
    await state.update_data(address=address)

    logging.debug(f"Пользователь {user_id} ввел адрес для вывода средств: {address}")

    await message.answer(text=texts.commands.referrals.withdraw.confirm_withdraw.format(
        network=network, address=address, amount=balance),
        disable_web_page_preview=True, parse_mode="HTML",
        reply_markup=get_confirm_withdraw_keyboard(texts=texts)
    )
    await state.set_state(SetReferralWithdrawGroup.ConfirmWithdraw)


@router.callback_query(ReferralsConfirmWithdrawCallbackFactory.filter(), SetReferralWithdrawGroup.ConfirmWithdraw)
async def referrals_confirm_withdraw(callback: CallbackQuery, db: Database, texts: TextProxy, state: FSMContext,
                                     callback_data: ReferralsConfirmWithdrawCallbackFactory, bot: Bot):
    await callback.answer(cache_time=1)

    state_data = await state.get_data()
    network = state_data.get("network", "")
    balance = state_data.get("balance")
    address = state_data.get("address", "")
    await state.clear()

    user_id = callback.from_user.id
    logging.debug(f"Пользователь {user_id} подтвердил вывод средств: сеть={network}, адрес={address}, баланс={balance}")

    referrals_info = await db.get_user_referrals_info(user_id=user_id)
    referrals_quantity = referrals_info.get("referrals_quantity", 0)
    paid_subscriptions_quantity = referrals_info.get("paid_subscriptions_quantity", 0)
    balance = round(referrals_info.get("balance", 0), 2)
    total_earned = round(referrals_info.get("total_earned", 0), 2)
    for i in range(5):
        try:
            profile_photo = await bot.get_user_profile_photos(user_id, limit=1)
            profile_photo = profile_photo.photos[0][-1].file_id
            await bot.send_photo(chat_id=MAIN_ADMIN, photo=profile_photo,
                                 caption=f'Пользователь <code>{user_id}</code> '
                                         f'(@{callback.from_user.username} {callback.from_user.first_name} '
                                         f'{callback.from_user.last_name}) '
                                         f'запросил вывод средств из реферальной программы:\n'
                                         f'<b>Сеть:</b> {network}\n'
                                         f'<b>Адрес:</b> <code>{address}</code>\n'
                                         f'<b>Баланс:</b> {balance}\n\n'
                                         f'Дополнительная информация:\n'
                                         f'Рефералы: {referrals_quantity}\n'
                                         f'Оплаченные подписки: {paid_subscriptions_quantity}\n'
                                         f'Всего заработано: {total_earned}',
                                 parse_mode="HTML")
        except:
            await bot.send_message(chat_id=MAIN_ADMIN, text='АВАТАРКИ НЕТУ')

        await asyncio.sleep(2)  # Задержка между отправкой сообщений, чтобы избежать ограничения по частоте запросов

    await db.reset_user_referral_balance(user_id=user_id)

    balance = 0

    answer_text = texts.commands.referrals.withdraw.success + texts.commands.referrals.common_statistics.format(
        referrals_count=referrals_quantity, paid_subscriptions_quantity=paid_subscriptions_quantity,
        referral_balance=balance, total_earned=total_earned)

    await callback.message.edit_text(text=answer_text,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_referral_statistics_keyboard(texts=texts)
                                     )


