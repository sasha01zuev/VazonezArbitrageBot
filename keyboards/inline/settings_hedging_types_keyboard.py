from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetHedgingTypesCallbackFactory, SetFuturesHedgingCallbackFactory, \
    SetMarginHedgingCallbackFactory, SetLoanHedgingCallbackFactory


def get_settings_hedging_types_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=texts.keyboard.settings.hedging_types.futures_hedging_type,
        callback_data=SetHedgingTypesCallbackFactory(hedging_type="futures_hedging")
    )

    builder.button(
        text=texts.keyboard.settings.hedging_types.margin_hedging_type,
        callback_data=SetHedgingTypesCallbackFactory(hedging_type="margin_hedging")
    )

    builder.button(
        text=texts.keyboard.settings.hedging_types.loan_hedging_type,
        callback_data=SetHedgingTypesCallbackFactory(hedging_type="loan_hedging")
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)

    return builder.as_markup()


def get_settings_futures_hedging_keyboard(texts: TextProxy, futures_hedging: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    hedging_only_text = f"✅ {texts.keyboard.settings.hedging_types.futures_hedging.hedging_only}" if futures_hedging else texts.keyboard.settings.hedging_types.futures_hedging.hedging_only
    all_pairs_text = f"✅ {texts.keyboard.settings.hedging_types.futures_hedging.all_pairs}" if not futures_hedging else texts.keyboard.settings.hedging_types.futures_hedging.all_pairs

    builder.button(
        text=hedging_only_text,
        callback_data=SetFuturesHedgingCallbackFactory(hedging_value=True)
    )

    builder.button(
        text=all_pairs_text,
        callback_data=SetFuturesHedgingCallbackFactory(hedging_value=False)
    )

    builder.add(back_button(texts=texts, callback_data="settings:hedging_types"))

    builder.adjust(1)

    return builder.as_markup()


def get_settings_margin_hedging_keyboard(texts: TextProxy, margin_hedging: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    hedging_only_text = f"✅ {texts.keyboard.settings.hedging_types.margin_hedging.hedging_only}" if margin_hedging else texts.keyboard.settings.hedging_types.margin_hedging.hedging_only
    all_pairs_text = f"✅ {texts.keyboard.settings.hedging_types.margin_hedging.all_pairs}" if not margin_hedging else texts.keyboard.settings.hedging_types.margin_hedging.all_pairs

    builder.button(
        text=hedging_only_text,
        callback_data=SetMarginHedgingCallbackFactory(hedging_value=True)
    )

    builder.button(
        text=all_pairs_text,
        callback_data=SetMarginHedgingCallbackFactory(hedging_value=False)
    )

    builder.add(back_button(texts=texts, callback_data="settings:hedging_types"))

    builder.adjust(1)

    return builder.as_markup()


def get_settings_loan_hedging_keyboard(texts: TextProxy, loan_hedging: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    hedging_only_text = f"✅ {texts.keyboard.settings.hedging_types.loan_hedging.hedging_only}" if loan_hedging else texts.keyboard.settings.hedging_types.loan_hedging.hedging_only
    all_pairs_text = f"✅ {texts.keyboard.settings.hedging_types.loan_hedging.all_pairs}" if not loan_hedging else texts.keyboard.settings.hedging_types.loan_hedging.all_pairs

    builder.button(
        text=hedging_only_text,
        callback_data=SetLoanHedgingCallbackFactory(hedging_value=True)
    )

    builder.button(
        text=all_pairs_text,
        callback_data=SetLoanHedgingCallbackFactory(hedging_value=False)
    )

    builder.add(back_button(texts=texts, callback_data="settings:hedging_types"))

    builder.adjust(1)

    return builder.as_markup()