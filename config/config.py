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


# ЦЕНА ПОДПИСОК
SUBSCRIPTION_PRICE = {
    "inter_exchange": {
        "one_week": 35,
        "one_month": 65,
        "three_month": 120,
        "lifetime": 490,
    }
}

# АДРЕСА КОШЕЛЬКОВ
WALLETS_ADDRESS = {
    "BEP20": "0xEb56F637b2391879B5bcfabe4fcb19200836961D",
    "TRC20": "TY63t95ZU44bcDitmcMPuZqLpaaLYYkE3e",
}

