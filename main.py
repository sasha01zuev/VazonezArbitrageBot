import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage

import middlewares
from handlers import routers_list

from config import config
import betterlogging as blog

from middlewares import ThrottlingMiddleware
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str = "bot.log", max_bytes: int = 20 * 1024 * 1024, backup_count: int = 5):
    """
    Set up logging configuration for the application, including rotating file handler.

    Args:
        log_file (str): Path to the log file.
        max_bytes (int): Max size of log file before rotation (default 20MB).
        backup_count (int): How many backup files to keep.

    Returns:
        None
    """
    log_level = logging.INFO
    blog.basic_colorized_config(level=log_level)

    # Файл логов с ротацией
    rotating_file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8',
    )

    # Формат логов
    formatter = logging.Formatter(
        fmt="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    rotating_file_handler.setFormatter(formatter)

    # Получаем корневой логгер и добавляем хендлеры
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(rotating_file_handler)

    # Дополнительно логгируем в консоль (оставляем betterlogging)
    logger = logging.getLogger(__name__)
    logger.info("Логирование настроено. Бот запускается.")


async def main():
    setup_logging(log_file="logs/info.log", max_bytes=10 * 1024 * 1024)

    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    middlewares.setup(dp)

    # Регистрация роутеров
    dp.include_routers(*routers_list)

    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")
