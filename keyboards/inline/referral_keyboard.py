from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton

from . import ReferralsCallbackFactory, ReferralsStatisticsCallbackFactory, ReferralsConfirmWithdrawCallbackFactory, \
    ReferralsConvertToSubscriptionCallbackFactory
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

    builder.button(
        text=texts.keyboard.referrals.buttons.statistics.set_statistics,
        callback_data=ReferralsCallbackFactory(item="statistics").pack()
    )
    builder.add(back_button(texts=texts, callback_data="menu"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()


def get_referral_statistics_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=texts.keyboard.referrals.buttons.statistics.withdraw,
        callback_data=ReferralsStatisticsCallbackFactory(time="N", action="withdraw").pack()
    )
    builder.button(
        text=texts.keyboard.referrals.buttons.statistics.convert_to_subscription,
        callback_data=ReferralsStatisticsCallbackFactory(time="N", action="convert_to_subscription").pack()
    )
    builder.add(back_button(texts=texts, callback_data="referrals"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()


def get_confirm_withdraw_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=texts.keyboard.referrals.buttons.statistics.confirm_withdraw,
        callback_data=ReferralsConfirmWithdrawCallbackFactory(action="confirm").pack()
    )
    builder.add(back_button(texts=texts, callback_data="referrals:statistics"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()


def get_subscriptions_for_convert_keyboard(texts: TextProxy, subscriptions: dict,
                                           balance: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if balance >= subscriptions['one_week']:
        builder.button(
            text=texts.keyboard.subscriptions.inter_exchange.buttons.one_week + " - " + str(subscriptions['one_week']) + "$",
            callback_data=ReferralsConvertToSubscriptionCallbackFactory(time="one_week").pack()
        )
    if balance >= subscriptions['one_month']:
        builder.button(
            text=texts.keyboard.subscriptions.inter_exchange.buttons.one_month + " - " + str(subscriptions['one_month']) + "$",
            callback_data=ReferralsConvertToSubscriptionCallbackFactory(time="one_month").pack()
        )
    if balance >= subscriptions['three_month']:
        builder.button(
            text=texts.keyboard.subscriptions.inter_exchange.buttons.three_month + " - " + str(subscriptions['three_month']) + "$",
            callback_data=ReferralsConvertToSubscriptionCallbackFactory(time="three_month").pack()
        )
    if balance >= subscriptions['lifetime']:
        builder.button(
            text=texts.keyboard.subscriptions.inter_exchange.buttons.lifetime + " - " + str(subscriptions['lifetime']) + "$",
            callback_data=ReferralsConvertToSubscriptionCallbackFactory(time="lifetime").pack()
        )

    builder.add(back_button(texts=texts, callback_data="referrals:statistics"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()
