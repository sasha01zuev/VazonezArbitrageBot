from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.i18n import TextProxy


def get_main_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.keyboard.menu.buttons.arbitrage, callback_data="arbitrage")
    builder.button(text=texts.keyboard.menu.buttons.settings, callback_data="settings")
    builder.button(text=texts.keyboard.menu.buttons.referrals, callback_data="referrals")
    builder.button(text=texts.keyboard.menu.buttons.subscriptions, callback_data="subscriptions")
    builder.button(text=texts.keyboard.menu.buttons.support, url="https://t.me/ArbitrageScreenerSupportBot")
    builder.adjust(1)  # 1 кнопка в строке

    return builder.as_markup()
