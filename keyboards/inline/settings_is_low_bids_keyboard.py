from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetIsLowBidsCallbackFactory


def get_settings_is_low_bids_keyboard(texts: TextProxy, is_low_bids: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    show_is_low_bids = f"✅ {texts.keyboard.settings.is_low_bids.show_low_bids}" if is_low_bids else texts.keyboard.settings.is_low_bids.show_low_bids
    hide_low_bids = f"✅ {texts.keyboard.settings.is_low_bids.hide_low_bids}" if not is_low_bids else texts.keyboard.settings.is_low_bids.hide_low_bids

    builder.button(
        text=show_is_low_bids,
        callback_data=SetIsLowBidsCallbackFactory(is_low_bids=True)
    )

    builder.button(
        text=hide_low_bids,
        callback_data=SetIsLowBidsCallbackFactory(is_low_bids=False)
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(2, 1)

    return builder.as_markup()