from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import ExchangesCallbackFactory


def get_settings_exchanges_keyboard(texts: TextProxy, exchanges: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.button.buy_exchange,
        callback_data="None"
    )
    builder.button(
        text=texts.button.sell_exchange,
        callback_data="None"
    )

    for exchange_name, exchanges_callbacks in exchanges.items():
        for exchange_name_callback, value in exchanges_callbacks.items():
            builder.button(
                text=f"{exchange_name.capitalize()} {"✅" if value else "❌"}",
                callback_data=ExchangesCallbackFactory(exchange=exchange_name_callback, is_true=value).pack()
            )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(2)  # 2 buttons in a row

    return builder.as_markup()