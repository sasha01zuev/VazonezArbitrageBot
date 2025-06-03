from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, CopyTextButton
from .back_button import back_button
from utils.i18n import TextProxy
from .callback_factories import SetNetworkSpeedCallbackFactory


def get_settings_network_speed_keyboard(texts: TextProxy, network_speed: int = 5,
                                        show_undefined_networks: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Список значков и их соответствующих интервалов
    emoji_levels = ["⚡️", "🟢", "🟡", "🔴", "💀"]

    # Добавим кнопку ⚪️ если включен show_undefined_networks
    if show_undefined_networks:
        builder.button(
            text="⚪️ - ✅",
            callback_data="None"
        )

    # Добавим кнопки от 1 до 5
    for i in range(1, 6):
        emoji = emoji_levels[i - 1]
        # Показываем галочку, если уровень скорости <= выбранного значения
        status = "✅" if i <= network_speed else "❌"
        builder.button(
            text=f"{emoji} - {status}",
            callback_data=SetNetworkSpeedCallbackFactory(network_speed=i,
                                                         is_show_undefined_networks_chosen=False,
                                                         show_undefined_networks=show_undefined_networks)
        )

    builder.button(
        text=texts.keyboard.settings.network_speed.undefined_network_on if show_undefined_networks else texts.keyboard.settings.network_speed.undefined_network_off,
        callback_data=SetNetworkSpeedCallbackFactory(network_speed=network_speed,
                                                     is_show_undefined_networks_chosen=True,
                                                     show_undefined_networks=show_undefined_networks)
    )

    builder.add(back_button(texts=texts, callback_data="settings"))

    if show_undefined_networks:
        builder.adjust(6, 1)  # 1 buttons in a row
    else:
        builder.adjust(5, 1)

    return builder.as_markup()