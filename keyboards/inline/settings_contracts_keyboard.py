from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetContractsCallbackFactory


def get_settings_contracts_keyboard(texts: TextProxy, contracts: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    contracts_match_text = f"✅ {texts.keyboard.settings.contracts.contracts_match}" if contracts else texts.keyboard.settings.contracts.contracts_match
    all_pairs_text = f"✅ {texts.keyboard.settings.contracts.all_pairs}" if not contracts else texts.keyboard.settings.contracts.all_pairs

    builder.button(
        text=contracts_match_text,
        callback_data=SetContractsCallbackFactory(contracts_type=True)
    )

    builder.button(
        text=all_pairs_text,
        callback_data=SetContractsCallbackFactory(contracts_type=False)
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(2, 1)

    return builder.as_markup()