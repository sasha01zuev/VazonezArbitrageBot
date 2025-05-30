from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from utils.i18n import TextProxy


def back_button(texts: TextProxy, callback_data: Union[str, CallbackData] = "menu") -> InlineKeyboardButton:
    """
    Возвращает одну кнопку "назад" с указанным callback_data
    """
    return InlineKeyboardButton(text=texts.button.back, callback_data=callback_data)