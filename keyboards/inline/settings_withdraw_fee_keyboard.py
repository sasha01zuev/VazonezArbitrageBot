from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetWithdrawFeeCallbackFactory


def get_settings_withdraw_fee_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.withdraw_fee.set_max_withdraw_fee,
        callback_data=SetWithdrawFeeCallbackFactory(withdraw_fee_type="withdraw_fee")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)  # 1 buttons in a row

    return builder.as_markup()