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

    async def set_user_inter_exchange_profit(self, user_id: int, profit: float):
        """
        profit: float
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET profit = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, profit)
            logging.info(f"Обновлено значение профита для пользователя {user_id}: {profit}")
        except Exception as e:
            logging.exception(f"Ошибка обновления профита для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_volume(self, user_id: int, volume: int):
        """
        volume: int
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET volume = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, volume)
            logging.info(f"Обновлено значение объема для пользователя {user_id}: {volume}")
        except Exception as e:
            logging.exception(f"Ошибка обновления объема для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_network_speed(self, user_id: int, network_speed: int):
        """
        network_speed: int (1-5)
        От 1 до 5. 1 - до 2 минут. 2 - до 5 минут. 3 - до 20 минут. 4 - до 1 часа. 5 - больше одного часа
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET network_speed = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, network_speed)
            logging.info(f"Обновлено значение скорости сети для пользователя {user_id}: {network_speed}")
        except Exception as e:
            logging.exception(f"Ошибка обновления скорости сети для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_show_undefined_networks(self, user_id: int, show_undefined_networks: bool):
        """
        show_undefined_networks: bool
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET show_undefined_networks = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, show_undefined_networks)
            logging.info(f"Обновлено значение показа неопределенных сетей для пользователя {user_id}: {show_undefined_networks}")
        except Exception as e:
            logging.exception(f"Ошибка обновления показа неопределенных сетей для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_contracts(self, user_id: int, contracts: bool):
        """
        contracts:bool
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET contracts = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, contracts)
            logging.info(f"Обновлено значение контрактов для пользователя {user_id}: {contracts}")
        except Exception as e:
            logging.exception(f"Ошибка обновления контрактов для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_withdraw_fee(self, user_id: int, withdraw_fee: float):
        """
        withdraw_fee: float
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET withdraw_fee = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, withdraw_fee)
            logging.info(f"Обновлено значение комиссии за вывод для пользователя {user_id}: {withdraw_fee}")
        except Exception as e:
            logging.exception(f"Ошибка обновления комиссии за вывод для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_coin_volume_24h(self, user_id: int, coin_volume_24h: int,
                                                      coin_volume_24h_type: str):
        """
        coin_volume_24h: int
        coin_volume_24h_type: min_coin_volume_24h, max_coin_volume_24h
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET {coin_volume_24h_type} = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, coin_volume_24h)
            logging.info(f"Обновлено значение {coin_volume_24h_type} для пользователя {user_id}: {coin_volume_24h}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения {coin_volume_24h_type} для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_last_trade_time(self, user_id: int, last_trade_time: int,
                                                      last_trade_time_type: str):
        """
        Устанавливает время последней торговли для пользователя.
        :param user_id:
        :param last_trade_time:
        :param last_trade_time_type:
        :return:
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET {last_trade_time_type} = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, last_trade_time)
            logging.info(f"Обновлено значение {last_trade_time_type} для пользователя {user_id}: {last_trade_time}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения {last_trade_time_type} для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_notification(self, user_id: int, notification: bool):
        """
        notification: bool
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET notification = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, notification)
            logging.info(f"Обновлено значение уведомлений для пользователя {user_id}: {notification}")
        except Exception as e:
            logging.exception(f"Ошибка обновления уведомлений для пользователя {user_id}: {e}")