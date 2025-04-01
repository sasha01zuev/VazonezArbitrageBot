import logging

from aiogram import Bot

from config.config import ADMINS_ID


async def on_startup_notify(bot: Bot):
    for admin in ADMINS_ID:
        try:
            await bot.send_message(admin, "<b>***Это сообщение видят только админы***\n\n"
                                          "                                БОТ ЗАПУЩЕН</b>", parse_mode="HTML")
        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(bot: Bot):
    for admin in ADMINS_ID:
        try:
            await bot.send_message(admin, "***Это сообщение видят только админы***\n"
                                          "БОТ ВЫКЛЮЧЕН")
            logging.info("Бот выключен")
        except Exception as err:
            logging.exception(err)
