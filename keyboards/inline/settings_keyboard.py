from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SettingsCallbackFactory


def get_settings_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=texts.keyboard.settings.buttons.language, callback_data=SettingsCallbackFactory(item="language").pack())

    builder.button(text=texts.keyboard.settings.buttons.exchanges, callback_data=SettingsCallbackFactory(item="exchanges").pack())

    builder.button(text=texts.keyboard.settings.buttons.spread, callback_data=SettingsCallbackFactory(item="spread").pack())
    builder.button(text=texts.keyboard.settings.buttons.profit, callback_data=SettingsCallbackFactory(item="profit").pack())

    builder.button(text=texts.keyboard.settings.buttons.volume, callback_data=SettingsCallbackFactory(item="volume").pack())
    builder.button(text=texts.keyboard.settings.buttons.network_speed, callback_data=SettingsCallbackFactory(item="network_speed").pack())

    builder.button(text=texts.keyboard.settings.buttons.contracts, callback_data=SettingsCallbackFactory(item="contracts").pack())
    builder.button(text=texts.keyboard.settings.buttons.withdraw_fee, callback_data=SettingsCallbackFactory(item="withdraw_fee").pack())

    builder.button(text=texts.keyboard.settings.buttons.volume_24h, callback_data=SettingsCallbackFactory(item="coin_volume_24h").pack())
    builder.button(text=texts.keyboard.settings.buttons.last_trade_time, callback_data=SettingsCallbackFactory(item="last_trade_time").pack())

    builder.button(text=texts.keyboard.settings.buttons.notification, callback_data=SettingsCallbackFactory(item="notification").pack())
    builder.button(text=texts.keyboard.settings.buttons.is_low_bids,
                   callback_data=SettingsCallbackFactory(item="is_low_bids").pack())

    builder.button(text=texts.keyboard.settings.buttons.hedging_types, callback_data=SettingsCallbackFactory(item="hedging_types").pack())

    builder.button(text=texts.keyboard.settings.buttons.blacklist_types, callback_data=SettingsCallbackFactory(item="blacklist_types").pack())

    builder.add(back_button(texts=texts, callback_data="menu"))

    builder.adjust(1, 1, 2, 2, 2, 2, 2, 1, 1, 1)
    return builder.as_markup()
