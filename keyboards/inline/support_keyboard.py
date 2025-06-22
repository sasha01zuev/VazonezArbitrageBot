from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import ArbitrageMenuCallbackFactory


def get_support_keyboard(texts: TextProxy, callback_data: str = "menu") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.keyboard.menu.buttons.support, url="https://t.me/ArbitrageScreenerSupportBot")

    builder.add(back_button(texts=texts, callback_data=callback_data))

    builder.adjust(1)
    return builder.as_markup()