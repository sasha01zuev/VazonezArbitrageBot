from typing import List

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import (SetBlacklistTypesCallbackFactory, SetMarginHedgingCallbackFactory,
                                 SetLoanHedgingCallbackFactory, SetCoinsBlacklistCallbackFactory,
                                 SetCoinsBlacklistCoinCallbackFactory, SetCoinsInCoinsBlacklistCallbackFactory)


def get_settings_blacklist_types_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.blacklist_types.coins_blacklist_type,
        callback_data=SetBlacklistTypesCallbackFactory(blacklist_type="coins_blacklist")
    )

    builder.button(
        text=texts.keyboard.settings.blacklist_types.networks_blacklist_type,
        callback_data=SetBlacklistTypesCallbackFactory(blacklist_type="networks_blacklist")
    )

    builder.button(
        text=texts.keyboard.settings.blacklist_types.coin_for_exchange_blacklist_type,
        callback_data=SetBlacklistTypesCallbackFactory(blacklist_type="coin_for_exchange_blacklist")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)

    return builder.as_markup()


def get_settings_coins_blacklist_keyboard(texts: TextProxy, blacklist_coins: List[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.blacklist_types.coins_blacklist.add_coin,
        callback_data=SetCoinsBlacklistCallbackFactory(action="add_coin")
    )

    if blacklist_coins:
        builder.button(
            text=texts.keyboard.settings.blacklist_types.coins_blacklist.remove_coin,
            callback_data=SetCoinsBlacklistCallbackFactory(action="remove_coin")
        )

    builder.add(back_button(texts=texts, callback_data="settings:blacklist_types"))

    builder.adjust(1)

    return builder.as_markup()


def get_settings_coins_blacklist_add_coin_keyboard(texts: TextProxy, top_blacklisted_coins: List[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Эмодзи для цифр 1️⃣, 2️⃣, 3️⃣ и т.д. — максимум 10 (по желанию можно расширить)
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    if top_blacklisted_coins:
        builder.button(
            text=texts.button.most_often_blocked,
            callback_data="None"  # Заголовок, неактивная кнопка
        )

        for i, coin in enumerate(top_blacklisted_coins):
            emoji = number_emojis[i] if i < len(number_emojis) else f"{i + 1}."
            builder.button(
                text=f"{emoji} {coin}",
                callback_data=SetCoinsBlacklistCoinCallbackFactory(coin=coin)
            )

        builder.add(back_button(texts=texts, callback_data="set_blacklist_types:coins_blacklist"))

        builder.adjust(1)
    else:
        builder.add(back_button(texts=texts, callback_data="set_blacklist_types:coins_blacklist"))

        builder.adjust(1)

    return builder.as_markup()


def get_settings_coins_blacklist_remove_coin_keyboard(texts: TextProxy, blacklisted_coins: List[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Эмодзи для цифр 1️⃣, 2️⃣, 3️⃣ и т.д. — максимум 10 (по желанию можно расширить)
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    if blacklisted_coins:
        builder.button(
            text=texts.button.last_blocked,
            callback_data="None"  # Заголовок, неактивная кнопка
        )

        for i, coin in enumerate(blacklisted_coins):
            emoji = number_emojis[i] if i < len(number_emojis) else f"{i + 1}."
            builder.button(
                text=f"{emoji} {coin}",
                callback_data=SetCoinsInCoinsBlacklistCallbackFactory(coin=coin)
            )

        builder.add(back_button(texts=texts, callback_data="set_blacklist_types:coins_blacklist"))

        builder.adjust(1)
    else:
        builder.add(back_button(texts=texts, callback_data="set_blacklist_types:coins_blacklist"))

        builder.adjust(1)

    return builder.as_markup()
