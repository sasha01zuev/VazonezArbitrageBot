from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import ArbitrageMenuCallbackFactory


def get_arbitrage_menu_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.keyboard.arbitrage.buttons.inter_exchange,
                   callback_data=ArbitrageMenuCallbackFactory(arbitrage_type="inter_exchange").pack())

    builder.add(back_button(texts=texts, callback_data="menu"))

    builder.adjust(1)
    return builder.as_markup()