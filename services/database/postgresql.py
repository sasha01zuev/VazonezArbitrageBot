import asyncpg
from asyncpg.pool import Pool
import logging
from typing import Optional
from config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_NAME


class Database:
    def __init__(self, pool: Pool):
        self.pool = pool  # пул соединений

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            database=POSTGRES_NAME,
            port=POSTGRES_PORT
        )
        logging.info("✅ Подключение к PostgreSQL установлено.")
        return cls(pool)

    @staticmethod
    def format_args(sql: str, parameters: dict):
        """
        Форматирует SQL строку под параметры словаря:
        sql = "SELECT * FROM users WHERE "
        parameters = {"user_id": 123, "username": "admin"}
        → SELECT * FROM users WHERE user_id = $1 AND username = $2
        """
        sql += " AND ".join([f"{key} = ${i + 1}" for i, key in enumerate(parameters)])
        return sql, tuple(parameters.values())

    async def add_user(self, user_id: int, username: str, first_name: str, language: Optional[str] = 'ru') -> None:
        sql = """
        INSERT INTO users(id, username, first_name, language)
        VALUES($1, $2, $3, $4)
        ON CONFLICT (id) DO NOTHING;
        """
        try:
            await self.pool.execute(sql, user_id, username, first_name, language)
            logging.info(f"{user_id} - пользователь добавлен в базу")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении в базу:{e}")

    async def get_user(self, user_id: int):
        sql = "SELECT * FROM users WHERE id = $1"
        try:
            user = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получен пользователь: {user}")
            return user
        except Exception as e:
            logging.exception(f"Ошибка получения пользователя: {e}")
            return None

    async def get_user_language(self, user_id: int):
        sql = "SELECT language FROM users WHERE id = $1"
        try:
            language = await self.pool.fetchval(sql, user_id)
            logging.debug(f"Получен язык пользователя {user_id}: {language}")
            return language
        except Exception as e:
            logging.exception(f"Ошибка получения языка пользователя: {e}")
            return None

    async def set_user_language(self, user_id: int, language: str):
        """
        Languages: ru, en
        """
        sql = """
        UPDATE users SET language = $1 WHERE id = $2
        """
        try:
            await self.pool.execute(sql, language, user_id)
            logging.info(f"Обновлён язык пользователя {user_id} на {language}")
        except Exception as e:
            logging.exception(f"Ошибка при обновлении языка пользователя {user_id}: {e}")

    async def get_availability_user_subscriptions(self, user_id: int):
        sql = "SELECT * FROM user_subscriptions WHERE user_id = $1"
        try:
            user_subscriptions = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены подписки пользователя {user_id}: {user_subscriptions}")
            return user_subscriptions
        except Exception as e:
            logging.exception(f"Ошибка получения подписок пользователя: {e}")
            return None

    async def add_user_default_subscriptions(self, user_id: int):
        sql = f"""
        INSERT INTO user_subscriptions(user_id)
        VALUES($1);
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Подписки для пользователя {user_id} добавлены в базу данных.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении подписок в базу: {e}")

    async def get_user_subscription(self, user_id: int, subscription_type: str):
        """
        subscription_type: inter_exchange
        """

        sql = (f"SELECT {subscription_type} FROM user_subscriptions "
               f"WHERE (user_id = $1 AND {subscription_type} > NOW())")
        try:
            subscription = await self.pool.fetchval(sql, user_id)
            logging.debug(f"Получена подписка {subscription_type} пользователя {user_id}: {subscription}")
            return subscription
        except Exception as e:
            logging.exception(f"Ошибка получения подписки {subscription_type} пользователя {user_id}: {e}")
            return None

    async def get_availability_user_inter_exchange_exchanges(self, user_id: int):
        sql = "SELECT * FROM user_inter_exchange_exchanges WHERE user_id = $1"
        try:
            user_exchanges = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены биржи пользователя {user_id}: {user_exchanges}")
            return user_exchanges
        except Exception as e:
            logging.exception(f"Ошибка получения бирж пользователя: {e}")
            return None

    async def add_user_default_inter_exchange_exchanges(self, user_id):
        sql = f"""
        INSERT INTO user_inter_exchange_exchanges(user_id)
        VALUES($1);
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Межбиржевые биржи для пользователя {user_id} добавлены в базу данных.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении межбиржевых бирж в базу: {e}")

    async def get_user_inter_exchange_exchanges(self, user_id: int):
        sql = "SELECT * FROM user_inter_exchange_exchanges WHERE user_id = $1"
        try:
            exchanges = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены межбиржевые биржи пользователя {user_id}: {exchanges}")
            return exchanges
        except Exception as e:
            logging.exception(f"Ошибка получения межбиржевых бирж пользователя {user_id}: {e}")
            return None

    async def set_user_inter_exchange_exchange(self, user_id: int, exchange: str, value: bool):
        """
        exchange: binance, bybit, huobi, kucoin, mexc, okx, cryptocom,
                  bitmart, poloniex, bitget, gate, bingx, lbank, coinw
        """
        sql = f"""
        UPDATE user_inter_exchange_exchanges
        SET {exchange} = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, value)
            logging.info(f"Обновлено значение {exchange} для пользователя {user_id}: {value}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения {exchange} для пользователя {user_id}: {e}")

    async def get_user_inter_exchange_settings(self, user_id: int):
        sql = "SELECT * FROM user_inter_exchange_settings WHERE user_id = $1"
        try:
            user_exchanges = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены настройки межбиржевых бирж пользователя {user_id}: {user_exchanges}")
            return user_exchanges
        except Exception as e:
            logging.exception(f"Ошибка получения настроек межбиржевых бирж пользователя: {e}")
            return None

    async def add_user_default_inter_exchange_settings(self, user_id):
        sql = f"""
        INSERT INTO user_inter_exchange_settings(user_id)
        VALUES($1);
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Межбиржевые настройки для пользователя {user_id} добавлены в базу данных.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении межбиржевых настроек в базу: {e}")

    async def set_user_inter_exchange_spread(self, user_id: int, spread_type: str, spread: float):
        """
        spread_type: min_spread, max_spread
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET {spread_type} = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, spread)
            logging.info(f"Обновлено значение {spread_type} для пользователя {user_id}: {spread}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения {spread_type} для пользователя {user_id}: {e}")