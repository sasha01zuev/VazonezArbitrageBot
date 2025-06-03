from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetCoinVolume24hCallbackFactory


def get_settings_coin_volume_24h_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.coin_volume_24h.set_max_coin_volume_24h,
        callback_data=SetCoinVolume24hCallbackFactory(coin_volume_24h_type="max_coin_volume_24h")
    )
    builder.button(
        text=texts.keyboard.settings.coin_volume_24h.set_min_coin_volume_24h,
        callback_data=SetCoinVolume24hCallbackFactory(coin_volume_24h_type="min_coin_volume_24h")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)  # 1 buttons in a row

    return builder.as_markup()