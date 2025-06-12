from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from .back_button import back_button
from utils.i18n import TextProxy


def get_referrer_invite_notification_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=texts.keyboard.menu.buttons.referrals, callback_data="referrals")

    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()