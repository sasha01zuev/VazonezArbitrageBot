from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton

from .callback_factories import SubscriptionsArbitrageTypeCallbackFactory, SubscriptionsTypeCallbackFactory, \
    SubscriptionsPayCallbackFactory, SubscriptionsCancelMonitoringCallbackFactory
from .back_button import back_button
from utils.i18n import TextProxy


def subscriptions_arbitrage_type_keyboard_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=texts.keyboard.arbitrage.buttons.inter_exchange,
                   callback_data=SubscriptionsArbitrageTypeCallbackFactory(arbitrage_type="inter_exchange").pack())

    builder.add(back_button(texts=texts, callback_data="menu"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()


def subscriptions_type_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=texts.keyboard.subscriptions.inter_exchange.buttons.one_week,
                   callback_data=SubscriptionsTypeCallbackFactory(subscription_type="one_week",
                                                                  payment_type="auto").pack())

    builder.button(text=texts.keyboard.subscriptions.inter_exchange.buttons.one_month,
                   callback_data=SubscriptionsTypeCallbackFactory(subscription_type="one_month",
                                                                  payment_type="auto").pack())

    builder.button(text=texts.keyboard.subscriptions.inter_exchange.buttons.three_month,
                   callback_data=SubscriptionsTypeCallbackFactory(subscription_type="three_month",
                                                                  payment_type="auto").pack())

    builder.button(text=texts.keyboard.subscriptions.inter_exchange.buttons.lifetime,
                   callback_data=SubscriptionsTypeCallbackFactory(subscription_type="lifetime",
                                                                  payment_type="auto").pack())

    builder.button(text=texts.keyboard.subscriptions.manual_payment,
                   callback_data=SubscriptionsTypeCallbackFactory(subscription_type="manual_payment",
                                                                  payment_type="manual").pack())

    builder.add(back_button(texts=texts, callback_data="subscriptions"))
    builder.adjust(4, 1, 1)  # 1 button in a row
    return builder.as_markup()


def subscriptions_pay_keyboard(texts: TextProxy, subscription_type, arbitrage_type) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text=texts.keyboard.subscriptions.pay,
                   callback_data=SubscriptionsPayCallbackFactory(subscription_type=subscription_type,
                                                                 arbitrage_type=arbitrage_type).pack())
    builder.add(back_button(texts=texts, callback_data="subscriptions_arbitrage:inter_exchange"))
    builder.adjust(1)  # 1 button in a row
    return builder.as_markup()


def subscriptions_monitoring_keyboard(texts: TextProxy) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.keyboard.menu.buttons.support, url="https://t.me/ArbitrageScreenerSupportBot")
    builder.button(text=texts.keyboard.subscriptions.cancel_monitoring,
                   callback_data=SubscriptionsCancelMonitoringCallbackFactory(
                       action="cancel_monitoring"
                   ).pack())

    builder.add(back_button(texts=texts, callback_data="menu"))

    builder.adjust(1)
    return builder.as_markup()
