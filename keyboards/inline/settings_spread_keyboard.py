from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetSpreadCallbackFactory


def get_settings_spread_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.spread.set_max_spread,
        callback_data=SetSpreadCallbackFactory(spread_type="max_spread")
    )
    builder.button(
        text=texts.keyboard.settings.spread.set_min_spread,
        callback_data=SetSpreadCallbackFactory(spread_type="min_spread")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)  # 1 buttons in a row

    return builder.as_markup()