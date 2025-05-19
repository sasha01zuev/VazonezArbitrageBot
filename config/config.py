from environs import Env
from urllib.parse import quote_plus

env = Env()
env.read_env()

# Бот
BOT_TOKEN = env("BOT_TOKEN")
MAIN_ADMIN = int(env("MAIN_ADMIN"))
ADMINS_ID = env.list("ADMINS_ID")

# База данных
# Берём переменные из окружения
POSTGRES_USER = env("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = quote_plus(env("POSTGRES_PASSWORD", "vazonez01"))  # экранирует символы типа @ : %
POSTGRES_HOST = env("POSTGRES_HOST", "localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", 5432)
POSTGRES_NAME = env("POSTGRES_DB", "arbitrage_bot_db")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

