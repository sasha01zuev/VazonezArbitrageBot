from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

from .back_button import back_button
from .callback_factories import LanguageCallbackFactory
from utils.i18n import TextProxy


def get_back_keyboard(texts: TextProxy, callback_data: Union[str, CallbackData] = "menu") -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(back_button(texts=texts, callback_data=callback_data))

    builder.adjust(1)  # 1 кнопка в строке

    return builder.as_markup()