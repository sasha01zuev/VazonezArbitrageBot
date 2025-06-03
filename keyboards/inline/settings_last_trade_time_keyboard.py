from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetLastTradeTimeCallbackFactory


def get_settings_last_trade_time_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.last_trade_time.set_max_last_trade_time,
        callback_data=SetLastTradeTimeCallbackFactory(last_trade_time_type="max_last_trade_time")
    )
    builder.button(
        text=texts.keyboard.settings.last_trade_time.set_min_last_trade_time,
        callback_data=SetLastTradeTimeCallbackFactory(last_trade_time_type="min_last_trade_time")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)  # 1 buttons in a row

    return builder.as_markup()