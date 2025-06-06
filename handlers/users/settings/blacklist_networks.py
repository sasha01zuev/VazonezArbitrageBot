import logging

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import (SetBlacklistTypesCallbackFactory, SetNetworksBlacklistCallbackFactory,
                              SetNetworksBlacklistNetworkCallbackFactory,
                              SetNetworksInNetworksBlacklistCallbackFactory,
                              get_settings_networks_blacklist_keyboard,
                              get_settings_networks_blacklist_add_network_keyboard,
                              get_settings_networks_blacklist_remove_networks_keyboard
                              )
from services.database.postgresql import Database
from states import SetBlacklistNetworksActionGroup
from utils.i18n import TextProxy

router = Router()

TELEGRAM_MESSAGE_LIMIT = 4096
ELLIPSIS = "..."


def format_blacklist_message(blacklist_coins: list[str], header_text: str) -> str:
    header = header_text
    base_length = len(header)
    networks_text = ""
    total_length = base_length

    for i, network in enumerate(blacklist_coins):
        # добавляем запятую и пробел, если это не первая сеть
        separator = ", " if i > 0 else ""
        part = f"<b>{separator}{network}</b>"
        new_length = total_length + len(part)

        # если следующая сеть не влезает — добавляем многоточие и выходим
        if new_length + len(ELLIPSIS) > TELEGRAM_MESSAGE_LIMIT:
            networks_text += ELLIPSIS
            break

        networks_text += part
        total_length = new_length

    return header + networks_text


@router.callback_query(SetBlacklistTypesCallbackFactory.filter(F.blacklist_type == "networks_blacklist"),
                       StateFilter("*"))
async def networks_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                             bot: Bot, db: Database):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistNetworksActionGroup.SetAddNetwork:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление сети в чёрный список")
        elif await state.get_state() == SetBlacklistNetworksActionGroup.SetRemoveNetwork:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление сетей из чёрного списка")
        else:
            logging.debug(f"Очищаем состояние {await state.get_state()} для пользователя {callback.from_user.id}")
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_networks = user_settings['blacklist_networks']
    logging.debug(f"User {user_id} current blacklist networks: {blacklist_networks}")
    if not blacklist_networks:
        text_answer = texts.commands.settings.blacklist_types.networks_blacklist.no_networks_in_blacklist
    else:
        text_answer = format_blacklist_message(
            blacklist_coins=blacklist_networks,
            header_text=texts.commands.settings.blacklist_types.networks_blacklist.current_networks_blacklist
        )

    await callback.message.edit_text(text=text_answer,
                                     disable_web_page_preview=True, parse_mode="HTML",
                                     reply_markup=get_settings_networks_blacklist_keyboard(
                                         texts=texts, blacklist_networks=blacklist_networks)
                                     )


@router.callback_query(SetNetworksBlacklistCallbackFactory.filter(), StateFilter("*"))
async def action_networks_blacklist(callback: CallbackQuery, texts: TextProxy, state: FSMContext, bot: Bot,
                                    db: Database, callback_data: SetNetworksBlacklistCallbackFactory):
    if await state.get_state() is not None:
        if await state.get_state() == SetBlacklistNetworksActionGroup.SetAddNetwork:
            logging.debug(f"Пользователь {callback.from_user.id} отменил добавление сети в чёрный список")
        elif await state.get_state() == SetBlacklistNetworksActionGroup.SetRemoveNetwork:
            logging.debug(f"Пользователь {callback.from_user.id} отменил удаление сетей из чёрного списка")
        else:
            await callback.message.answer(text=texts.commands.state.canceled_state,
                                          disable_web_page_preview=True, parse_mode="HTML")
    await state.clear()

    await callback.answer(cache_time=1)

    user_id = callback.from_user.id
    action = callback_data.action

    if action == "add_network":

        top_blacklisted_networks = await db.get_top_blacklist_networks(user_id=user_id, top_n=5)
        network_names = [network for network, _ in top_blacklisted_networks]
        logging.debug(f"Top blacklisted networks: {top_blacklisted_networks}")

        text_answer = texts.commands.settings.blacklist_types.networks_blacklist.add_networks_blacklist
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_networks_blacklist_add_network_keyboard(
                                             texts=texts,
                                             top_blacklisted_networks=network_names)
                                         )
        await state.set_state(SetBlacklistNetworksActionGroup.SetAddNetwork)
    elif action == "remove_network":
        text_answer = texts.commands.settings.blacklist_types.networks_blacklist.remove_networks_blacklist
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_networks = user_settings['blacklist_networks'][-5:][::-1]
        logging.debug(f"User {user_id} current blacklist networks: {blacklist_networks}")
        await callback.message.edit_text(text=text_answer,
                                         disable_web_page_preview=True, parse_mode="HTML",
                                         reply_markup=get_settings_networks_blacklist_remove_networks_keyboard(
                                             texts=texts,
                                             blacklisted_networks=blacklist_networks)
                                         )
        await state.set_state(SetBlacklistNetworksActionGroup.SetRemoveNetwork)


@router.callback_query(SetNetworksBlacklistNetworkCallbackFactory.filter(),
                       SetBlacklistNetworksActionGroup.SetAddNetwork)
async def add_network_to_networks_blacklist_callback(callback: CallbackQuery, texts: TextProxy, state: FSMContext,
                                                     bot: Bot, db: Database,
                                                     callback_data: SetNetworksBlacklistNetworkCallbackFactory):
    await state.clear()

    user_id = callback.from_user.id
    network = callback_data.network.upper()

    await callback.answer(cache_time=1, text=texts.callback.successfully_added)

    logging.debug(f"Пользователь {user_id} пытается добавить сеть {network} в черный список")

    await db.add_blacklist_networks(user_id=user_id, network=network)

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_networks = user_settings['blacklist_networks']

    if not blacklist_networks:
        await action_networks_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db,
                                        callback_data=SetNetworksBlacklistCallbackFactory(action="add_network"))
    else:
        await networks_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db)


@router.callback_query(SetNetworksInNetworksBlacklistCallbackFactory.filter(),
                       SetBlacklistNetworksActionGroup.SetRemoveNetwork)
async def remove_network_from_networks_blacklist_callback(callback: CallbackQuery, texts: TextProxy,
                                                          state: FSMContext, bot: Bot, db: Database,
                                                          callback_data: SetNetworksInNetworksBlacklistCallbackFactory):
    await state.clear()

    user_id = callback.from_user.id
    network = callback_data.network.upper()

    await callback.answer(cache_time=1, text=texts.callback.successfully_removed)

    logging.debug(f"Пользователь {user_id} пытается удалить сеть {network} из черного списка")

    await db.remove_blacklist_networks(user_id=user_id, network=network)

    user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
    blacklist_networks = user_settings['blacklist_networks']

    if blacklist_networks:
        await action_networks_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db,
                                        callback_data=SetNetworksBlacklistCallbackFactory(action="remove_network"))
    else:
        await networks_blacklist(callback=callback, texts=texts, state=state, bot=bot, db=db)


@router.message(SetBlacklistNetworksActionGroup.SetAddNetwork)
async def add_network_to_networks_blacklist_message(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                                    db: Database):
    user_id = message.from_user.id

    try:
        network = message.text.strip().upper()

        if not network:
            raise ValueError("Network name cannot be empty")

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_networks = user_settings['blacklist_networks']
        top_blacklisted_networks = await db.get_top_blacklist_networks(user_id=user_id, top_n=5)
        network_names = [network for network, _ in top_blacklisted_networks]
        logging.debug(f"Топ сетей в черном списке: {top_blacklisted_networks}")

        if network in blacklist_networks:
            await message.answer(
                texts.commands.settings.blacklist_types.networks_blacklist.errors.already_in_blacklist.format(
                    network=network),
                reply_markup=get_settings_networks_blacklist_add_network_keyboard(texts=texts,
                                                                                  top_blacklisted_networks=network_names),
                disable_web_page_preview=True, parse_mode="HTML"
            )
        elif len(network) >= 15:
            await message.answer(
                texts.commands.settings.blacklist_types.networks_blacklist.errors.network_name_too_long,
                reply_markup=get_settings_networks_blacklist_add_network_keyboard(texts=texts,
                                                                                  top_blacklisted_networks=network_names),
                disable_web_page_preview=True, parse_mode="HTML")
        else:
            await db.add_blacklist_networks(user_id=user_id, network=network)
            await message.answer(
                texts.commands.settings.blacklist_types.networks_blacklist.success.network_added.format(
                    network=network),
                disable_web_page_preview=True, parse_mode="HTML"
            )

            blacklist_networks.append(network)

            if not blacklist_networks:
                text_answer = texts.commands.settings.blacklist_types.networks_blacklist.no_networks_in_blacklist
            else:
                text_answer = format_blacklist_message(
                    blacklist_coins=blacklist_networks,
                    header_text=texts.commands.settings.blacklist_types.networks_blacklist.current_networks_blacklist
                )

            await message.answer(text=text_answer,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_settings_networks_blacklist_keyboard(texts=texts,
                                                                                       blacklist_networks=blacklist_networks)
                                 )
            await state.clear()
    except Exception as e:
        top_blacklisted_networks = await db.get_top_blacklist_networks(user_id=user_id, top_n=5)
        network_names = [network for network, _ in top_blacklisted_networks]
        logging.debug(f"Топ сетей в черном списке: {top_blacklisted_networks}")

        await message.answer(texts.commands.settings.blacklist_types.networks_blacklist.errors.unexpected_error,
                             reply_markup=get_settings_networks_blacklist_add_network_keyboard(texts=texts,
                                                                                               top_blacklisted_networks=network_names),
                             disable_web_page_preview=True, parse_mode="HTML")
        logging.error(f"Ошибка при добавлении сети в черный список: {e}")


@router.message(SetBlacklistNetworksActionGroup.SetRemoveNetwork)
async def remove_network_from_networks_blacklist_message(message: Message, texts: TextProxy, state: FSMContext, bot: Bot,
                                                   db: Database):
    user_id = message.from_user.id

    try:
        network = message.text.strip().upper()

        if not network:
            raise ValueError("Network name cannot be empty")

        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_networks = user_settings['blacklist_networks'][-5:][::-1]

        if network not in blacklist_networks:
            await message.answer(
                texts.commands.settings.blacklist_types.networks_blacklist.errors.not_in_blacklist.format(network=network),
                reply_markup=get_settings_networks_blacklist_remove_networks_keyboard(texts=texts,
                                                                                     blacklisted_networks=blacklist_networks),
                disable_web_page_preview=True, parse_mode="HTML"
            )
        else:
            await db.remove_blacklist_networks(user_id=user_id, network=network)
            await message.answer(
                texts.commands.settings.blacklist_types.networks_blacklist.success.network_removed.format(network=network),
                disable_web_page_preview=True, parse_mode="HTML"
            )

            blacklist_networks.remove(network)

            if not blacklist_networks:
                text_answer = texts.commands.settings.blacklist_types.networks_blacklist.no_networks_in_blacklist
            else:
                text_answer = format_blacklist_message(
                    blacklist_coins=blacklist_networks,
                    header_text=texts.commands.settings.blacklist_types.networks_blacklist.current_networks_blacklist
                )

            await message.answer(text=text_answer,
                                 disable_web_page_preview=True, parse_mode="HTML",
                                 reply_markup=get_settings_networks_blacklist_keyboard(texts=texts,
                                                                                       blacklist_networks=blacklist_networks)
                                 )
            await state.clear()
    except Exception as e:
        user_settings = await db.get_user_inter_exchange_settings(user_id=user_id)
        blacklist_networks = user_settings['blacklist_networks'][-5:][::-1]

        logging.error(f"Ошибка при удалении сети из черного списка: {e}")
        await message.answer(texts.commands.settings.blacklist_types.networks_blacklist.errors.unexpected_error,
                             reply_markup=get_settings_networks_blacklist_remove_networks_keyboard(texts=texts,
                                                                                                  blacklisted_networks=blacklist_networks),
                             disable_web_page_preview=True, parse_mode="HTML")
