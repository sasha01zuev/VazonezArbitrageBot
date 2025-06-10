import logging
from csv import excel

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from pyexpat.errors import messages

from keyboards.inline import (SetBlacklistTypesCallbackFactory, get_settings_coins_blacklist_keyboard,
                              SetCoinsBlacklistCallbackFactory, get_settings_coins_blacklist_add_coin_keyboard,
                              get_settings_coins_blacklist_remove_coin_keyboard, SetCoinsBlacklistCoinCallbackFactory,
                              SetCoinsInCoinsBlacklistCallbackFactory,
                              get_settings_coin_for_exchange_blacklist_keyboard,
                              SetCoinForExchangeBlacklistCallbackFactory,
                              get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard,
                              get_settings_coin_for_exchange_blacklist_add_coin_keyboard,
                              get_settings_coin_for_exchange_blacklist_select_exchange_keyboard,
                              SelectExchangeForCoinForExchangeBlacklistCallbackFactory,
                              SetCoinForExchangeBlacklistCoinForExchangeCoinCallbackFactory)
from services.database.postgresql import Database
from states import SetBlacklistCoinsActionGroup, SetBlacklistCoinForExchangeActionGroup
from utils.i18n import TextProxy

router = Router()

TELEGRAM_MESSAGE_LIMIT = 4096
ELLIPSIS = "..."


def format_blacklist_message(blacklist_coins: list[str], header_text: str) -> str:
    header = header_text
    base_length = len(header)
    coin_for_exchange_text = ""
    total_length = base_length

    for i, coin in enumerate(blacklist_coins):
        # добавляем запятую и пробел, если это не первая монета
        separator = ", " if i > 0 else ""
        part = f"<b>{separator}{coin}</b>"
        new_length = total_length + len(part)

        # если следующая монета не влезает — добавляем многоточие и выходим
        if new_length + len(ELLIPSIS) > TELEGRAM_MESSAGE_LIMIT:
            coin_for_exchange_text += ELLIPSIS
            break

        coin_for_exchange_text += part
        total_length = new_length

    return header + coin_for_exchange_text


def get_exchanges_for_coin(coin: str, available: list[str]) -> list[str]:
    matches = [entry.split("-")[1] for entry in available if entry.startswith(f"{coin}-")]
    return matches


@router.callback_query(SetBlacklistTypesCallbackFactory.filter(F.blacklist_type == "coin_for_exchange_blacklist"),
                       StateFilter("*"))
async def coin_for_exchange_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                      db: Database):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты к бирже в черный список")
        elif await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']
    logging.debug(f"User {user_id} current blacklist coin for exchange: {blacklist_coin_for_exchange}")

    if not blacklist_coin_for_exchange:
        text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.no_coin_for_exchange_blacklist
    else:
        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coin_for_exchange,
            header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
        )

    await callback.message.edit_text(text=text_answer,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                                         texts=texts,
                                         blacklist_coin_for_exchange=blacklist_coin_for_exchange)
                                     )


@router.callback_query(SetCoinForExchangeBlacklistCallbackFactory.filter(), StateFilter("*"))
async def action_coin_for_exchange_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                             db: Database,
                                             callback_data: SetCoinForExchangeBlacklistCallbackFactory):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты в черный список")
        elif await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id
    action = callback_data.action

    if action == "add_coin_for_exchange":
        text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.add_coin_for_exchange_blacklist
        top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id, top_n=5)
        coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in top_blacklisted_coin_for_exchange]
        logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                                             texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
                                         )
        await state.set_state(SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange)
    elif action == "remove_coin_for_exchange":
        text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.remove_coin_for_exchange_blacklist
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklisted_coin_for_exchange = user_settings['blacklist_coin_for_exchange'][-5:][::-1]
        logging.debug(f"User {user_id} current blacklist coin_for_exchange: {blacklisted_coin_for_exchange}")
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard(
                                             texts=texts, blacklisted_coin_for_exchange=blacklisted_coin_for_exchange)
                                         )
        await state.set_state(SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange)


@router.message(SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange)
async def set_message_to_add_coin_for_exchange(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                               db: Database):
    user_id = message.from_user.id
    user_message = message.text

    coin = user_message.strip().upper() if (len(user_message.split("-")) == 1
                                            and len(user_message.split(" ")) == 1) else ""
    coin_exchange = user_message.strip() if (len(user_message.split("-")) == 2
                                             and len(user_message.split(" ")) == 1) else ""

    logging.debug(f"Coin: {coin}, Coin for exchange: {coin_exchange}")
    logging.debug(f"Пользователь {user_id} ввел монету для добавления в черный список монет к бирже: {user_message}")

    try:
        if coin:
            if len(coin) > 15:
                top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id,
                                                                                                 top_n=5)
                coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in
                                           top_blacklisted_coin_for_exchange]
                logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

                await message.answer(
                    text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.add.more_than_15_symbols,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                        texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
                )
                return
            exchanges = dict(await db.get_user_inter_exchange_exchanges(user_id=user_id))
            exchanges.pop("user_id")

            user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
            blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']

            filtered_exchanges = {
                name: data
                for name, data in exchanges.items()
                if f"{coin.upper()}-{name.capitalize()}" not in blacklist_coin_for_exchange
            }
            logging.debug(f"Доступные биржи для монеты {coin}: {filtered_exchanges}")

            await message.answer(
                text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.select_exchange.format(
                    coin=coin),
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_coin_for_exchange_blacklist_select_exchange_keyboard(
                    texts=texts, coin=coin, exchanges=filtered_exchanges, action="add"))
            await state.clear()
        elif coin_exchange:
            coin = coin_exchange.split("-")[0].strip().upper()
            exchange = coin_exchange.split("-")[1].strip().capitalize()

            if len(coin) > 15:
                top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id,
                                                                                                 top_n=5)
                coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in
                                           top_blacklisted_coin_for_exchange]
                logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

                await message.answer(
                    text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.add.more_than_15_symbols,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                        texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
                )
                return
            exchanges = dict(await db.get_user_inter_exchange_exchanges(user_id=user_id))
            exchanges.pop("user_id")

            if exchange.lower() not in exchanges:
                top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id,
                                                                                                 top_n=5)
                coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in
                                           top_blacklisted_coin_for_exchange]
                logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

                await message.answer(
                    text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.add.errors.wrong_exchange,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                        texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
                )
                return

            user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
            blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']
            logging.debug(f"Черный список монет для биржи пользователя {user_id}: {blacklist_coin_for_exchange}")

            if f"{coin}-{exchange}" in blacklist_coin_for_exchange:
                top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id,
                                                                                                 top_n=5)
                coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in
                                           top_blacklisted_coin_for_exchange]
                logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

                await message.answer(
                    text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.add.coin_for_exchange_already_exists.format(
                        coin=coin, exchange=exchange),
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                        texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
                )
                return

            await db.add_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=f"{coin}-{exchange}")

            blacklist_coin_for_exchange.append(f"{coin}-{exchange}")

            text_answer = format_blacklist_message(
                blacklist_coins=blacklist_coin_for_exchange,
                header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.success.add_coin_for_exchange.format(
                    coin=coin,
                    exchange=exchange) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
            )

            await message.answer(
                text=text_answer,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                    texts=texts, blacklist_coin_for_exchange=blacklist_coin_for_exchange)
            )

            await state.clear()
        else:
            raise ValueError("Неверный формат ввода. Ожидалось название монеты или монеты для биржи.")
    except Exception as e:
        top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id, top_n=5)
        coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in top_blacklisted_coin_for_exchange]
        logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

        await message.answer(
            text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.add.wrong_input_format,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
        )
        logging.error(f"Ошибка при обработке ввода пользователя {user_id}: {e}")
        return


@router.callback_query(SelectExchangeForCoinForExchangeBlacklistCallbackFactory.filter(), StateFilter("*"))
async def select_exchange_coin_for_exchange_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                                      bot: Bot,
                                                      db: Database,
                                                      callback_data: SelectExchangeForCoinForExchangeBlacklistCallbackFactory):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты в черный список")
        elif await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    logging.debug(f"Callback data: {callback_data}")

    exchange = callback_data.exchange.capitalize()
    coin = callback_data.coin
    action = callback_data.action

    user_id = callback.from_user.id

    if action == "add":
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']
        logging.debug(f"Черный список монет для биржи пользователя {user_id}: {blacklist_coin_for_exchange}")

        if f"{coin}-{exchange}" in blacklist_coin_for_exchange:
            top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id,
                                                                                             top_n=5)
            coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in top_blacklisted_coin_for_exchange]
            logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

            await callback.message.edit_text(
                text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.add.coin_for_exchange_already_exists.format(
                    coin=coin, exchange=exchange),
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_coin_for_exchange_blacklist_add_coin_keyboard(
                    texts=texts, top_blacklisted_coin_for_exchange=coin_for_exchange_names)
            )
            return

        await db.add_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=f"{coin}-{exchange}")

        top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id, top_n=5)
        coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in top_blacklisted_coin_for_exchange]
        logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

        blacklist_coin_for_exchange.append(f"{coin}-{exchange}")

        await callback.answer(cache_time=1, text=texts.callback.successfully_added)

        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coin_for_exchange,
            header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
        )

        await callback.message.edit_text(
            text=text_answer,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                texts=texts, blacklist_coin_for_exchange=coin_for_exchange_names)
        )
    elif action == "remove":
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']
        logging.debug(f"Черный список монет для биржи пользователя {user_id}: {blacklist_coin_for_exchange}")

        await db.remove_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=f"{coin}-{exchange}")

        blacklist_coin_for_exchange.remove(f"{coin}-{exchange}")

        await callback.answer(cache_time=1, text=texts.callback.successfully_removed)
        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coin_for_exchange,
            header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
        )

        await callback.message.edit_text(
            text=text_answer,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                texts=texts, blacklist_coin_for_exchange=blacklist_coin_for_exchange)
        )


@router.message(SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange)
async def set_message_to_remove_coin_for_exchange(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                                  db: Database):
    user_id = message.from_user.id
    user_message = message.text

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']

    logging.debug(f"User {user_id} current blacklist coin for exchange: {blacklist_coin_for_exchange}")

    coin = user_message.strip().upper() if (len(user_message.split("-")) == 1
                                            and len(user_message.split(" ")) == 1) else ""
    coin_exchange = user_message.strip() if (len(user_message.split("-")) == 2
                                             and len(user_message.split(" ")) == 1) else ""

    logging.debug(f"Coin: {coin}, Coin for exchange: {coin_exchange}")
    logging.debug(f"Пользователь {user_id} ввел монету для удаления из черного списка монет к бирже: {user_message}")

    try:
        if coin:
            available_exchanges_for_coin = get_exchanges_for_coin(coin, blacklist_coin_for_exchange)
            logging.debug(f"Доступные биржи для монеты {coin}: {available_exchanges_for_coin}")

            if not available_exchanges_for_coin:
                if not blacklist_coin_for_exchange:
                    text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.no_available_exchanges.format(
                        coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.no_coin_for_exchange_blacklist
                else:
                    text_answer = format_blacklist_message(
                        blacklist_coins=blacklist_coin_for_exchange,
                        header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.no_available_exchanges.format(
                            coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
                    )

                await message.answer(
                    text=text_answer,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard(
                        texts=texts, blacklisted_coin_for_exchange=blacklist_coin_for_exchange[-5:][::-1])
                )
                return

            exchanges_dict = {exchange: 1 for exchange in set(available_exchanges_for_coin)}
            await message.answer(
                text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.select_exchange.format(
                    coin=coin),
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_coin_for_exchange_blacklist_select_exchange_keyboard(
                    texts=texts, coin=coin, exchanges=exchanges_dict, action="remove"))
            await state.clear()
        elif coin_exchange:
            coin = coin_exchange.split("-")[0].strip().upper()
            exchange = coin_exchange.split("-")[1].strip().capitalize()
            logging.debug(f"Пользователь {user_id} ввел монету для удаления из черного списка монет к бирже: {coin_exchange}")

            available_exchanges_for_coin = get_exchanges_for_coin(coin, blacklist_coin_for_exchange)
            logging.debug(f"Доступные биржи для монеты {coin}: {available_exchanges_for_coin}")

            if not available_exchanges_for_coin:
                if not blacklist_coin_for_exchange:
                    text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.no_available_exchanges.format(
                        coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.no_coin_for_exchange_blacklist
                else:
                    text_answer = format_blacklist_message(
                        blacklist_coins=blacklist_coin_for_exchange,
                        header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.no_available_exchanges.format(
                            coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
                    )

                await message.answer(
                    text=text_answer,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard(
                        texts=texts, blacklisted_coin_for_exchange=blacklist_coin_for_exchange[-5:][::-1])
                )
                return

            if exchange not in available_exchanges_for_coin:
                if not blacklist_coin_for_exchange:
                    text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.wrong_exchange.format(exchange=exchange, coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.no_coin_for_exchange_blacklist
                else:
                    text_answer = format_blacklist_message(
                        blacklist_coins=blacklist_coin_for_exchange,
                        header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.wrong_exchange.format(exchange=exchange, coin=coin) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
                    )

                await message.answer(
                    text=text_answer,
                    disable_web_page_preview=True, parse_mode="HTML",
                    reply_markup=get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard(
                        texts=texts, blacklisted_coin_for_exchange=blacklist_coin_for_exchange[-5:][::-1])
                )
                return

            await db.remove_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=f"{coin}-{exchange}")
            blacklist_coin_for_exchange.remove(f"{coin}-{exchange}")

            text_answer = format_blacklist_message(
                blacklist_coins=blacklist_coin_for_exchange,
                header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.success.remove_coin_for_exchange.format(
                    coin=coin,
                    exchange=exchange) + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
            )
            await message.answer(
                text=text_answer,
                disable_web_page_preview=True, parse_mode="HTML",
                reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                    texts=texts, blacklist_coin_for_exchange=blacklist_coin_for_exchange)
            )

            await state.clear()
        else:
            raise ValueError("Неверный формат ввода. Ожидалось название монеты или монеты для биржи.")
    except Exception as e:

        if not blacklist_coin_for_exchange:
            text_answer = texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.wrong_input_format + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.no_coin_for_exchange_blacklist
        else:
            text_answer = format_blacklist_message(
                blacklist_coins=blacklist_coin_for_exchange,
                header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.errors.remove.wrong_input_format + texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
            )

        await message.answer(
            text=text_answer,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_remove_coin_for_exchange_keyboard(
                texts=texts, blacklisted_coin_for_exchange=blacklist_coin_for_exchange[-5:][::-1])
        )
        logging.error(f"Ошибка при обработке ввода пользователя {user_id}: {e}")
        return


@router.callback_query(SetCoinForExchangeBlacklistCoinForExchangeCoinCallbackFactory.filter(), StateFilter("*"))
async def select_coin_for_exchange_blacklist_callback(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                                      bot: Bot,
                                                      db: Database,
                                                      callback_data: SetCoinForExchangeBlacklistCoinForExchangeCoinCallbackFactory):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetAddCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты к бирже в черный список")
        elif await state.get_state() == SetBlacklistCoinForExchangeActionGroup.SetRemoveCoinForExchange:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты к бирже из черного списка")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    logging.debug(f"Callback data: {callback_data}")

    user_id = callback.from_user.id
    coin_for_exchange = callback_data.coin_for_exchange
    action = callback_data.action
    coin = coin_for_exchange.split("-")[0].strip().upper()
    exchange = coin_for_exchange.split("-")[1].strip().capitalize()

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coin_for_exchange = user_settings['blacklist_coin_for_exchange']
    logging.debug(f"Черный список монет для биржи пользователя {user_id}: {blacklist_coin_for_exchange}")

    if action == "add":
        await db.add_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=coin_for_exchange)

        top_blacklisted_coin_for_exchange = await db.get_top_blacklist_coin_for_exchange(user_id=user_id, top_n=5)
        coin_for_exchange_names = [coin_for_exchange for coin_for_exchange, _ in top_blacklisted_coin_for_exchange]
        logging.debug(f"Top blacklisted coin_for_exchange: {top_blacklisted_coin_for_exchange}")

        blacklist_coin_for_exchange.append(f"{coin}-{exchange}")

        await callback.answer(cache_time=1, text=texts.callback.successfully_added)
        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coin_for_exchange,
            header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
        )

        await callback.message.edit_text(
            text=text_answer,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                texts=texts, blacklist_coin_for_exchange=coin_for_exchange_names)
        )

    elif action == "remove":
        await db.remove_blacklist_coin_for_exchange(user_id=user_id, coin_for_exchange=coin_for_exchange)

        blacklist_coin_for_exchange.remove(f"{coin}-{exchange}")

        await callback.answer(cache_time=1, text=texts.callback.successfully_removed)

        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coin_for_exchange,
            header_text=texts.commands.settings.blacklist_types.coin_for_exchange_blacklist.current_coin_for_exchange_blacklist
        )

        await callback.message.edit_text(
            text=text_answer,
            disable_web_page_preview=True, parse_mode="HTML",
            reply_markup=get_settings_coin_for_exchange_blacklist_keyboard(
                texts=texts, blacklist_coin_for_exchange=blacklist_coin_for_exchange)
        )
