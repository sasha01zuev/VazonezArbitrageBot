from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetVolumeCallbackFactory


def get_settings_volume_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.volume.set_max_volume,
        callback_data=SetVolumeCallbackFactory(volume_type="volume")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)  # 1 buttons in a row

    return builder.as_markup()