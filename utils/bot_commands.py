from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

COMMANDS_RU = [
    BotCommand(command="start", description="▶️ Начать/Перезапустить бота"),
    BotCommand(command="menu", description="🏠 Главное меню"),
    BotCommand(command="arbitrage", description="📈 Информация по арбитражу"),
    BotCommand(command="settings", description="⚙️ Настройки"),
    BotCommand(command="language", description="🌐 Язык"),
    BotCommand(command="subscriptions", description="💳 Подписки"),
    BotCommand(command="referral_program", description="👥 Реферальная программа"),
]

COMMANDS_EN = [
    BotCommand(command="start", description="▶️ Start/Restart the bot"),
    BotCommand(command="menu", description="🏠 Main menu"),
    BotCommand(command="arbitrage", description="📈 Arbitrage information"),
    BotCommand(command="settings", description="⚙️ Settings"),
    BotCommand(command="language", description="🌐 Language"),
    BotCommand(command="subscriptions", description="💳 Subscriptions"),
    BotCommand(command="referral_program", description="👥 Referral program"),
]


async def set_user_bot_commands(bot: Bot, user_id: int, lang: str):
    if lang == "ru":
        await bot.set_my_commands(COMMANDS_RU, scope=BotCommandScopeChat(chat_id=user_id))
    elif lang == "en":
        await bot.set_my_commands(COMMANDS_EN, scope=BotCommandScopeChat(chat_id=user_id))