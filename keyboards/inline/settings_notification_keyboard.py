from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetNotificationCallbackFactory


def get_settings_notification_keyboard(texts: TextProxy, notification: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    notification_text = f"🔕 {texts.keyboard.settings.notification.inter_exchange}" if not notification else (
        f"🔔 {texts.keyboard.settings.notification.inter_exchange}")

    builder.button(
        text=notification_text,
        callback_data=SetNotificationCallbackFactory(notification=notification)
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    builder.adjust(1)

    return builder.as_markup()