import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import SettingsCallbackFactory, LanguageCallbackFactory, get_settings_exchanges_keyboard, \
    ExchangesCallbackFactory
from services.database.postgresql import Database
from utils.i18n import TextProxy

router = Router()


@router.callback_query(SettingsCallbackFactory.filter(F.item == "exchanges"), StateFilter("*"))
async def set_exchanges(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    user_id = callback.from_user.id

    inter_exchange_subscription = await db.get_user_subscription(user_id=user_id, subscription_type="inter_exchange")

    if inter_exchange_subscription:
        await callback.answer(cache_time=1)
        exchanges_dict = {}

        exchanges = dict(await db.get_user_inter_exchange_exchanges(user_id=user_id))
        exchanges.pop("user_id")

        logging.debug(f"User {user_id} биржи: {exchanges}")

        for exchange_name, value in exchanges.items():
            logging.debug(f"Биржа {exchange_name} имеет значение {value}")

            if "s_" in exchange_name:
                main_exchange_name = exchange_name.replace("s_", "")
                if main_exchange_name in exchanges_dict:
                    exchanges_dict[main_exchange_name][exchange_name] = value
                else:
                    exchanges_dict[main_exchange_name] = {exchange_name: value}
            else:
                exchanges_dict[exchange_name] = {exchange_name: value}
        logging.debug(f"Биржи пользователя {user_id} в словаре:\n"
                      f"{exchanges_dict}")

        await callback.message.edit_text(texts.commands.settings.exchanges,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_exchanges_keyboard(texts=texts, exchanges=exchanges_dict)
                                         )
    else:
        await callback.answer(cache_time=1, text=texts.callback.no_subscription)


@router.callback_query(ExchangesCallbackFactory.filter(F.exchange), StateFilter("*"))
async def selected_exchange(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                          callback_data: ExchangesCallbackFactory):
    if await state.get_state() is not None:
        logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
        await callback.message.answer(text=texts.commands.state.canceled_state,
                             disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=2, text=texts.callback.exchange_changed)
    logging.debug(f"Callback data: {callback_data}")

    user_id = callback.from_user.id
    exchange_name = callback_data.exchange
    exchanges_dict = {}

    is_true = True if not callback_data.is_true else False
    await db.set_user_inter_exchange_exchange(user_id=user_id, exchange=exchange_name, value=is_true)

    logging.debug(f"Пользователь {callback.from_user.id} выбрал биржу {exchange_name}")

    exchanges = dict(await db.get_user_inter_exchange_exchanges(user_id=user_id))
    exchanges.pop("user_id")

    logging.debug(f"User {user_id} биржи: {exchanges}")

    for exchange_name, value in exchanges.items():
        logging.debug(f"Биржа {exchange_name} имеет значение {value}")

        if "s_" in exchange_name:
            main_exchange_name = exchange_name.replace("s_", "")
            if main_exchange_name in exchanges_dict:
                exchanges_dict[main_exchange_name][exchange_name] = value
            else:
                exchanges_dict[main_exchange_name] = {exchange_name: value}
        else:
            exchanges_dict[exchange_name] = {exchange_name: value}
    logging.debug(f"Биржи пользователя {user_id} в словаре:\n"
                  f"{exchanges_dict}")

    await callback.message.edit_text(texts.commands.settings.exchanges,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_exchanges_keyboard(texts=texts, exchanges=exchanges_dict)
                                     )
