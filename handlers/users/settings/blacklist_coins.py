import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.inline import (SetBlacklistTypesCallbackFactory, get_settings_coins_blacklist_keyboard,
                              SetCoinsBlacklistCallbackFactory, get_settings_coins_blacklist_add_coin_keyboard,
                              get_settings_coins_blacklist_remove_coin_keyboard, SetCoinsBlacklistCoinCallbackFactory,
                              SetCoinsInCoinsBlacklistCallbackFactory)
from services.database.postgresql import Database
from states import SetBlacklistCoinsActionGroup
from utils.i18n import TextProxy

router = Router()

TELEGRAM_MESSAGE_LIMIT = 4096
ELLIPSIS = "..."


def format_blacklist_message(blacklist_coins: list[str], header_text: str) -> str:
    header = header_text
    base_length = len(header)
    coins_text = ""
    total_length = base_length

    for i, coin in enumerate(blacklist_coins):
        # добавляем запятую и пробел, если это не первая монета
        separator = ", " if i > 0 else ""
        part = f"<b>{separator}{coin}</b>"
        new_length = total_length + len(part)

        # если следующая монета не влезает — добавляем многоточие и выходим
        if new_length + len(ELLIPSIS) > TELEGRAM_MESSAGE_LIMIT:
            coins_text += ELLIPSIS
            break

        coins_text += part
        total_length = new_length

    return header + coins_text


@router.callback_query(SetBlacklistTypesCallbackFactory.filter(F.blacklist_type == "coins_blacklist"), StateFilter("*"))
async def coins_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinsActionGroup.SetAddCoin:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты в черный список")
        elif await state.get_state() == SetBlacklistCoinsActionGroup.SetRemoveCoin:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coins = user_settings['blacklist_coins']
    logging.debug(f"User {user_id} current blacklist coins: {blacklist_coins}")

    if not blacklist_coins:
        text_answer = texts.commands.settings.blacklist_types.coins_blacklist.no_coins_in_blacklist
    else:
        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_coins,
            header_text=texts.commands.settings.blacklist_types.coins_blacklist.current_coins_blacklist
        )

    await callback.message.edit_text(text=text_answer,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_coins_blacklist_keyboard(texts=texts,
                                                                                        blacklist_coins=blacklist_coins)
                                     )


@router.callback_query(SetCoinsBlacklistCallbackFactory.filter(), StateFilter("*"))
async def action_coins_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot, db: Database,
                                 callback_data: SetCoinsBlacklistCallbackFactory):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistCoinsActionGroup.SetAddCoin:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление монеты в черный список")
        elif await state.get_state() == SetBlacklistCoinsActionGroup.SetRemoveCoin:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление монеты")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id
    action = callback_data.action

    if action == "add_coin":
        text_answer = texts.commands.settings.blacklist_types.coins_blacklist.add_coins_blacklist
        top_blacklisted_coins = await db.get_top_blacklist_coins(user_id=user_id, top_n=5)
        coin_names = [coin for coin, _ in top_blacklisted_coins]
        logging.debug(f"Top blacklisted coins: {top_blacklisted_coins}")
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_coins_blacklist_add_coin_keyboard(texts=texts,
                                                                                                     top_blacklisted_coins=coin_names)
                                         )
        await state.set_state(SetBlacklistCoinsActionGroup.SetAddCoin)
    elif action == "remove_coin":
        text_answer = texts.commands.settings.blacklist_types.coins_blacklist.remove_coins_blacklist
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklisted_coins = user_settings['blacklist_coins'][-5:][::-1]
        logging.debug(f"User {user_id} current blacklist coins: {blacklisted_coins}")
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_coins_blacklist_remove_coin_keyboard(texts=texts,
                                                                                                        blacklisted_coins=blacklisted_coins)
                                         )
        await state.set_state(SetBlacklistCoinsActionGroup.SetRemoveCoin)


@router.callback_query(SetCoinsBlacklistCoinCallbackFactory.filter(), SetBlacklistCoinsActionGroup.SetAddCoin)
async def add_coin_to_coins_blacklist_callback(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                               db: Database,
                                               callback_data: SetCoinsBlacklistCallbackFactory):
    await state.clear()

    user_id = callback.from_user.id
    coin = callback_data.coin.upper()

    await callback.answer(cache_time=1, text=texts.callback.successfully_added)

    logging.debug(f"Пользователь {user_id} пытается добавить монету {coin} в черный список")

    await db.add_blacklist_coins(user_id=user_id, coin=coin)

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coins = user_settings['blacklist_coins']

    if not blacklist_coins:
        await action_coins_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db,
                                     callback_data=SetCoinsBlacklistCallbackFactory(action="add_coin"))
    else:
        await coins_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db)


@router.callback_query(SetCoinsInCoinsBlacklistCallbackFactory.filter(), SetBlacklistCoinsActionGroup.SetRemoveCoin)
async def remove_coin_from_coins_blacklist_callback(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                                    bot: Bot,
                                                    db: Database,
                                                    callback_data: SetCoinsInCoinsBlacklistCallbackFactory):
    await state.clear()

    user_id = callback.from_user.id
    coin = callback_data.coin

    await callback.answer(cache_time=1, text=texts.callback.successfully_removed)

    logging.debug(f"Пользователь {user_id} пытается удалить монету {coin} из черного списка")

    await db.remove_blacklist_coins(user_id=user_id, coin=coin.upper())

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_coins = user_settings['blacklist_coins']

    if blacklist_coins:
        await action_coins_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db,
                                     callback_data=SetCoinsBlacklistCallbackFactory(action="remove_coin"))
    else:
        await coins_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db)


@router.message(SetBlacklistCoinsActionGroup.SetAddCoin)
async def add_coin_to_coins_blacklist_message(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                              db: Database):
    user_id = message.from_user.id

    try:
        coin = message.text.strip().upper()

        if not coin:
            raise ValueError("Coin name cannot be empty")

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_coins = user_settings['blacklist_coins']
        top_blacklisted_coins = await db.get_top_blacklist_coins(user_id=user_id, top_n=5)
        coin_names = [coin for coin, _ in top_blacklisted_coins]
        logging.debug(f"Top blacklisted coins: {top_blacklisted_coins}")

        if coin in blacklist_coins:
            await message.answer(
                texts.commands.settings.blacklist_types.coins_blacklist.errors.already_in_blacklist.format(coin=coin),
                reply_markup=get_settings_coins_blacklist_add_coin_keyboard(texts=texts,
                                                                            top_blacklisted_coins=coin_names),
                disable_web_page_preview=True, parse_mode="HTML"
            )
        elif len(coin) >= 15:
            await message.answer(texts.commands.settings.blacklist_types.coins_blacklist.errors.coin_name_too_long,
                                 reply_markup=get_settings_coins_blacklist_add_coin_keyboard(texts=texts,
                                                                                             top_blacklisted_coins=coin_names),
                                 disable_web_page_preview=True, parse_mode="HTML")
        else:
            await db.add_blacklist_coins(user_id=user_id, coin=coin)
            await message.answer(
                texts.commands.settings.blacklist_types.coins_blacklist.success.coin_added.format(coin=coin),
                disable_web_page_preview=True, parse_mode="HTML"
            )

            blacklist_coins.append(coin)

            if not blacklist_coins:
                text_answer = texts.commands.settings.blacklist_types.coins_blacklist.no_coins_in_blacklist
            else:
                text_answer = format_blacklist_message(
                    blacklist_coins=blacklist_coins,
                    header_text=texts.commands.settings.blacklist_types.coins_blacklist.current_coins_blacklist
                )

            await message.answer(text=text_answer,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_settings_coins_blacklist_keyboard(texts=texts,
                                                                                    blacklist_coins=blacklist_coins)
                                 )
            await state.clear()
    except Exception as e:
        top_blacklisted_coins = await db.get_top_blacklist_coins(user_id=user_id, top_n=5)
        coin_names = [coin for coin, _ in top_blacklisted_coins]
        logging.debug(f"Top blacklisted coins: {top_blacklisted_coins}")

        await message.answer(texts.commands.settings.blacklist_types.coins_blacklist.errors.unexpected_error,
                             reply_markup=get_settings_coins_blacklist_add_coin_keyboard(texts=texts,
                                                                                         top_blacklisted_coins=coin_names),
                             disable_web_page_preview=True, parse_mode="HTML")
        logging.error(f"Ошибка при добавлении монеты в черный список: {e}")


@router.message(SetBlacklistCoinsActionGroup.SetRemoveCoin)
async def remove_coin_from_coins_blacklist_message(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                                   db: Database):
    user_id = message.from_user.id

    try:
        coin = message.text.strip().upper()

        if not coin:
            raise ValueError("Coin name cannot be empty")

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_coins = user_settings['blacklist_coins']

        if coin not in blacklist_coins:
            await message.answer(
                texts.commands.settings.blacklist_types.coins_blacklist.errors.not_in_blacklist.format(coin=coin),
                reply_markup=get_settings_coins_blacklist_remove_coin_keyboard(texts=texts,
                                                                               blacklisted_coins=blacklist_coins[-5:][
                                                                                                 ::-1]),
                disable_web_page_preview=True, parse_mode="HTML"
            )
        else:
            await db.remove_blacklist_coins(user_id=user_id, coin=coin)
            await message.answer(
                texts.commands.settings.blacklist_types.coins_blacklist.success.coin_removed.format(coin=coin),
                disable_web_page_preview=True, parse_mode="HTML"
            )

            blacklist_coins.remove(coin)

            if blacklist_coins:
                text_answer = format_blacklist_message(
                    blacklist_coins=blacklist_coins,
                    header_text=texts.commands.settings.blacklist_types.coins_blacklist.current_coins_blacklist
                )
            else:
                text_answer = texts.commands.settings.blacklist_types.coins_blacklist.no_coins_in_blacklist

            await message.answer(text=text_answer,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_settings_coins_blacklist_keyboard(texts=texts,
                                                                                    blacklist_coins=blacklist_coins)
                                 )
            await state.clear()

    except Exception as e:
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_coins = user_settings['blacklist_coins']

        logging.error(f"Ошибка при удалении монеты из черного списка: {e}")
        await message.answer(texts.commands.settings.blacklist_types.coins_blacklist.errors.unexpected_error,
                             disable_web_page_preview=True, parse_mode="HTML",
                             reply_markup=get_settings_coins_blacklist_remove_coin_keyboard(texts=texts,
                                                                                            blacklisted_coins=blacklist_coins[-5:][::-1]))
