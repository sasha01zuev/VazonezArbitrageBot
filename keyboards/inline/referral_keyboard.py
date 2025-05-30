from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy


def get_referral_keyboard(texts: TextProxy, user_referral_link: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.referrals.buttons.invite,
        switch_inline_query=user_referral_link

    )

    builder.button(
        text=texts.keyboard.referrals.buttons.copy,
        copy_text=CopyTextButton(text=user_referral_link)
    )
    builder.add(back_button(texts=texts, callback_data="menu"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()
