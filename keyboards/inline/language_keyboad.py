from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

from .back_button import back_button
from .callback_factories import LanguageCallbackFactory
from utils.i18n import TextProxy


def get_language_keyboard(texts: TextProxy, current_lang: str, is_from_settings: bool,
                          is_start_command: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    logging.debug(f"Ru {texts.keyboard.language.buttons.russian}")
    logging.debug(f"En {texts.keyboard.language.buttons.english}")

    languages = {
        "ru": texts.keyboard.language.buttons.russian,
        "en": texts.keyboard.language.buttons.english
        # Добавь другие языки при необходимости
    }

    for code, label in languages.items():
        display_text = f"✅ {label}" if code == current_lang else label
        builder.button(
            text=display_text,
            callback_data=LanguageCallbackFactory(item=code).pack()
        )

    if not is_start_command:
        builder.add(back_button(texts=texts, callback_data="settings" if is_from_settings else "menu"))

    builder.adjust(2, 1)  # 1 кнопка в строке

    return builder.as_markup()