import json

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

    async def add_user_subscription(self, user_id: int, arbitrage_type: str, subscription_time: str):
        """
        Продлевает подписку пользователя:
        - если подписка ещё активна — прибавляет время к текущей дате окончания
        - если уже истекла — ставит подписку от текущего момента

        :param user_id: ID пользователя
        :param arbitrage_type: Название поля подписки (например: 'inter_exchange')
        :param subscription_time: строка интервала, например '1 week', '1 month', '3 month', '999 year'
        """
        sql = f"""
        UPDATE user_subscriptions
        SET {arbitrage_type} = 
            CASE
                WHEN {arbitrage_type} > NOW() THEN {arbitrage_type} + INTERVAL '{subscription_time}'
                ELSE NOW() + INTERVAL '{subscription_time}'
            END
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Подписка [{arbitrage_type}] пользователя {user_id} продлена на {subscription_time}")
        except Exception as e:
            logging.exception(f"Ошибка при продлении подписки [{arbitrage_type}] для пользователя {user_id}: {e}")

    async def delete_user_subscription(self, user_id: int, subscription_type: str):
        """
        Сбрасывает подписку пользователя.
        :param user_id: ID пользователя
        :param subscription_type: Название поля подписки (например: 'inter_exchange')
        """
        sql = f"""
        UPDATE user_subscriptions
        SET {subscription_type} = NOW()
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Подписка [{subscription_type}] пользователя {user_id} сброшена")
        except Exception as e:
            logging.exception(f"Ошибка при сбросе подписки [{subscription_type}] для пользователя {user_id}: {e}")

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

    async def get_user_referral_info(self, user_id: int):
        """
        Получает информацию о рефералах пользователя.
        :param user_id: ID пользователя
        :return: Словарь с информацией о рефералах или None в случае ошибки
        """
        sql = "SELECT * FROM referrals_info WHERE user_id = $1"
        try:
            referral_info = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получена реферальная информация пользователя {user_id}: {referral_info}")
            return referral_info
        except Exception as e:
            logging.exception(f"Ошибка получения реферальной информации пользователя {user_id}: {e}")
            return None

    async def set_default_user_referral_info(self, user_id: int):
        """
        Устанавливает значения по умолчанию для реферальной информации пользователя.
        :param user_id: ID пользователя
        """
        sql = """
        INSERT INTO referrals_info(user_id)
        VALUES($1)
        ON CONFLICT (user_id) DO NOTHING;
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Реферальная информация для пользователя {user_id} добавлена в базу данных.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении реферальной информации в базу: {e}")

    async def get_user_wallets(self, user_id: int):
        """
        Получает информацию о кошельках пользователя.
        :param user_id: ID пользователя
        :return: Словарь с информацией о кошельках или None в случае ошибки
        """
        sql = "SELECT * FROM user_wallets WHERE user_id = $1"
        try:
            wallets = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены кошельки пользователя {user_id}: {wallets}")
            return wallets
        except Exception as e:
            logging.exception(f"Ошибка получения кошельков пользователя {user_id}: {e}")
            return None

    async def set_default_user_wallets(self, user_id: int, wallets: Optional[dict] = None):
        """
        Устанавливает значения по умолчанию для кошельков пользователя.
        :param user_id: ID пользователя
        :param wallets: кошельки пользователя в формате словаря:
        """
        sql = """
        INSERT INTO user_wallets(user_id, usdt_bep20_address, usdt_bep20_key, usdt_trc20_address, usdt_trc20_key)
        VALUES($1, $2, $3, $4, $5);
        """
        try:
            await self.pool.execute(sql, user_id,
                                    wallets["usdt_bep20_address"],
                                    wallets["usdt_bep20_key"],
                                    wallets["usdt_trc20_address"],
                                    wallets["usdt_trc20_key"]
                                    )
            logging.info(f"Кошельки для пользователя {user_id} добавлены в базу данных.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении кошельков в базу: {e}")

    async def set_new_user_wallets(self, user_id: int, wallets: dict):
        """
        Обновляет кошельки пользователя (каждое поле отдельно)
        """
        sql = """
        UPDATE user_wallets
        SET
            usdt_bep20_address = $2,
            usdt_bep20_key = $3,
            usdt_trc20_address = $4,
            usdt_trc20_key = $5,
            created_at = NOW(),
            updated_at = NOW()
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql,
                                    user_id,
                                    wallets["usdt_bep20_address"],
                                    wallets["usdt_bep20_key"],
                                    wallets["usdt_trc20_address"],
                                    wallets["usdt_trc20_key"]
                                    )
            logging.info(f"Кошельки для пользователя {user_id} обновлены.")
        except Exception as e:
            logging.exception(f"{user_id} — ошибка обновления кошельков: {e}")

    async def get_all_monitoring_wallets(self):
        """
        Получает информацию о всех кошельках пользователей для мониторинга.
        :return: Список словарей с информацией о кошельках или None в случае ошибки
        """
        sql = "SELECT * FROM user_wallets WHERE expires_at > NOW()"
        try:
            wallets = await self.pool.fetch(sql)
            logging.debug(f"Получены все кошельки для мониторинга: {wallets}")
            return wallets
        except Exception as e:
            logging.exception(f"Ошибка получения всех кошельков для мониторинга: {e}")
            return None

    async def get_next_available_wallet_delay(self):
        """
        Получает время ожидания до ближайшего освобождения кошелька.
        :return: Кортеж (минуты, секунды) или None, если кошельков нет
        """
        sql = """
            SELECT expires_at - NOW() AS time_left
            FROM user_wallets
            WHERE expires_at > NOW()
            ORDER BY expires_at ASC
            LIMIT 1
        """
        try:
            result = await self.pool.fetchrow(sql)
            if result and result['time_left']:
                time_left = result['time_left']
                total_seconds = time_left.total_seconds()
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                logging.debug(f"Ближайшее время ожидания до освобождения кошелька: {minutes} мин {seconds} сек")
                return minutes, seconds
            else:
                logging.debug("Нет активных кошельков — все слоты свободны")
                return None
        except Exception as e:
            logging.exception(f"Ошибка при получении ближайшего времени освобождения кошелька: {e}")
            return None

    async def add_user_wallets_to_monitoring(self, user_id: int, time: str, subscription_price: int,
                                             subscription_type: str, arbitrage_type: str):
        """
        Добавляет кошелек пользователя в мониторинг, если срок действия истёк.
        :param user_id: ID пользователя
        :param time: время в формате 'HH:MM:SS'
        :param subscription_price: Цена подписки
        :param subscription_type: Тип подписки (например, 'one_month', 'three_month', 'lifetime')
        :param arbitrage_type: Тип арбитража (например, 'inter_exchange')
        """
        sql = f"""
        UPDATE user_wallets
        SET expires_at = NOW() + INTERVAL '{time}', subscription_price = $2, arbitrage_type = $3, subscription_type = $4 
        WHERE user_id = $1 AND expires_at < NOW();
        """
        try:
            result = await self.pool.execute(sql, user_id, subscription_price, arbitrage_type, subscription_type)
            if result == "UPDATE 0":
                logging.info(f"Кошелек пользователя {user_id} уже находится в мониторинге. Обновление не требуется.")
            else:
                logging.info(f"Кошелек пользователя {user_id} добавлен в мониторинг на {time} "
                             f"с ценой подписки {subscription_price}, "
                             f"типом подписки {subscription_type} и типом арбитража {arbitrage_type}.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при добавлении кошелька в мониторинг: {e}")

    async def get_user_wallets_in_monitoring(self, user_id: int):
        """
        Получает информацию о кошельках пользователя в мониторинге.
        :param user_id: ID пользователя
        :return: Словарь с информацией о кошельках или None в случае ошибки
        """
        sql = "SELECT * FROM user_wallets WHERE user_id = $1 AND expires_at > NOW()"
        try:
            wallets = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получены кошельки пользователя {user_id} в мониторинге: {wallets}")
            return wallets
        except Exception as e:
            logging.exception(f"Ошибка получения кошельков пользователя {user_id} в мониторинге: {e}")
            return None

    async def get_user_available_time_wallet(self, user_id: int):
        """
        Получает время ожидания до ближайшего освобождения кошелька.
        :return: Кортеж (минуты, секунды) или None, если кошельков нет
        """
        sql = """
            SELECT expires_at - NOW() AS time_left
            FROM user_wallets
            WHERE expires_at > NOW() AND user_id = $1
        """
        try:
            result = await self.pool.fetchrow(sql, user_id)
            if result and result['time_left']:
                time_left = result['time_left']
                total_seconds = time_left.total_seconds()
                minutes = int(total_seconds // 60)
                seconds = int(total_seconds % 60)
                logging.debug(f"Ближайшее время ожидания до освобождения кошелька пользователя {user_id}: "
                              f"{minutes} мин {seconds} сек")
                return minutes, seconds
            else:
                logging.debug(f"Нет активных кошельков для пользователя {user_id}")
                return None
        except Exception as e:
            logging.exception(f"Ошибка при получении ближайшего времени освобождения кошелька: {e}")
            return None

    async def update_time_reminder(self, user_id: int, time_reminder: dict):
        """
        Обновляет поле time_reminder (JSONB) для пользователя.
        """
        sql = "UPDATE user_wallets SET time_reminder = $1 WHERE user_id = $2"
        try:
            await self.pool.execute(sql, json.dumps(time_reminder), user_id)
            logging.info(f"Обновлены уведомления time_reminder для {user_id}")
        except Exception as e:
            logging.exception(f"Ошибка при обновлении time_reminder: {e}")

    async def update_payment_status(self, user_id: int, payment_status: dict):
        """
        Обновляет поле payment_status (JSONB) для пользователя.
        """
        sql = "UPDATE user_wallets SET payment_status = $1 WHERE user_id = $2"
        try:
            await self.pool.execute(sql, json.dumps(payment_status), user_id)
            logging.info(f"Обновлен payment_status для {user_id}")
        except Exception as e:
            logging.exception(f"Ошибка при обновлении payment_status: {e}")

    async def get_all_expired_wallets(self):
        """
        Получает информацию о всех кошельках пользователей, срок действия которых истёк.
        :return: Список словарей с информацией о кошельках или None в случае ошибки
        """
        sql = "SELECT * FROM user_wallets WHERE expires_at < NOW()"
        try:
            expired_wallets = await self.pool.fetch(sql)
            logging.debug(f"Получены все истекшие кошельки: {expired_wallets}")
            return expired_wallets
        except Exception as e:
            logging.exception(f"Ошибка получения всех истекших кошельков: {e}")
            return None

    async def reset_user_wallets_in_monitoring(self, user_id: int, usdt_bep_20_address: str, usdt_bep_20_key: str,
                                               usdt_trc_20_address: str, usdt_trc_20_key: str, time_reminder: dict,
                                               payment_status: dict):
        sql = f"""
        UPDATE user_wallets
        SET usdt_bep20_address = $2, usdt_bep20_key = $3, usdt_trc20_address = $4, usdt_trc20_key = $5,
        created_at = NOW(), expires_at = NOW(), subscription_price = 0, arbitrage_type = 'inter_exchange',
        subscription_type = 'one_month', time_reminder = $6, payment_status = $7
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, usdt_bep_20_address, usdt_bep_20_key,
                                    usdt_trc_20_address, usdt_trc_20_key, json.dumps(time_reminder),
                                    json.dumps(payment_status))

            logging.info(f"Кошельки пользователя {user_id} сброшены в мониторинге. \n"
                         f"usdt_bep_20_address: {usdt_bep_20_address}\n"
                         f"usdt_bep_20_key: {usdt_bep_20_key}\n"
                         f"usdt_trc_20_address: {usdt_trc_20_address}\n"
                         f"usdt_trc_20_key: {usdt_trc_20_key}\n"
                         f"time_reminder: {time_reminder}\n"
                         f"payment_status: {payment_status}")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при сбросе мониторинга кошельков: {e}")

    async def cancel_user_wallets_in_monitoring(self, user_id: int):
        """
        Отменяет мониторинг кошельков пользователя.
        :param user_id: ID пользователя
        """
        sql = """
        UPDATE user_wallets
        SET expires_at = NOW()
        WHERE user_id = $1 AND expires_at > NOW();
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Мониторинг кошельков пользователя {user_id} отменен.")
        except Exception as e:
            logging.exception(f"{user_id} - ошибка при отмене мониторинга кошельков: {e}")

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

    async def set_user_inter_exchange_is_low_bids(self, user_id: int, is_low_bids: bool):
        """
        is_low_bids: bool
        """
        sql = """
        UPDATE user_inter_exchange_settings
        SET is_low_bids = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, is_low_bids)
            logging.info(f"Обновлено значение is_low_bids для пользователя {user_id}: {is_low_bids}")
        except Exception as e:
            logging.exception(f"Ошибка обновления is_low_bids для пользователя {user_id}: {e}")

    async def set_user_inter_exchange_hedging(self, user_id, hedging_value: bool, hedging_type: str):
        """
        hedging_value: bool
        hedging_type: hedging_futures, margin_hedging, loan_hedging
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET {hedging_type} = $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, hedging_value)
            logging.info(f"Обновлено значение {hedging_type} для пользователя {user_id}: {hedging_value}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения {hedging_type} для пользователя {user_id}: {e}")

    async def add_blacklist_coins(self, user_id: int, coin: str):
        """
        coin: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_coins = array_append(blacklist_coins, $2)
        WHERE user_id = $1 AND NOT ($2 = ANY(blacklist_coins));
        """
        try:
            await self.pool.execute(sql, user_id, coin)
            logging.info(f"Обновлено значение blacklist_coins для пользователя {user_id}: {coin}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения blacklist_coins для пользователя {user_id}: {e}")

    async def remove_blacklist_coins(self, user_id: int, coin: str):
        """
        coin: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_coins = array_remove(blacklist_coins, $2)
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, coin)
            logging.info(f"Удалено значение blacklist_coins для пользователя {user_id}: {coin}")
        except Exception as e:
            logging.exception(f"Ошибка удаления значения blacklist_coins для пользователя {user_id}: {e}")

    async def get_top_blacklist_coins(self, user_id: int, top_n: int = 5) -> list[tuple[str, int]]:
        sql = """
        WITH user_blacklist AS (
            SELECT unnest(blacklist_coins) AS coin
            FROM user_inter_exchange_settings
            WHERE user_id = $1
        ),
        all_blacklists AS (
            SELECT unnest(blacklist_coins) AS coin
            FROM user_inter_exchange_settings
        )
        SELECT coin, COUNT(*) AS frequency
        FROM all_blacklists
        WHERE coin NOT IN (SELECT coin FROM user_blacklist)
        GROUP BY coin
        ORDER BY frequency DESC
        LIMIT $2;
        """
        try:
            top_coins = await self.pool.fetch(sql, user_id, top_n)
            logging.debug(
                f"Получены топ {top_n} монет из чёрного списка, которых нет у пользователя {user_id}: {top_coins}")
            return [(row['coin'], row['frequency']) for row in top_coins]
        except Exception as e:
            logging.exception(f"Ошибка получения топ монет из черного списка без учёта пользователя {user_id}: {e}")
            return []

    async def add_blacklist_networks(self, user_id: int, network: str):
        """
        network: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_networks = array_append(blacklist_networks, $2)
        WHERE user_id = $1 AND NOT ($2 = ANY(blacklist_networks));
        """
        try:
            await self.pool.execute(sql, user_id, network)
            logging.info(f"Обновлено значение blacklist_networks для пользователя {user_id}: {network}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения blacklist_networks для пользователя {user_id}: {e}")

    async def remove_blacklist_networks(self, user_id: int, network: str):
        """
        network: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_networks = array_remove(blacklist_networks, $2)
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, network)
            logging.info(f"Удалено значение blacklist_networks для пользователя {user_id}: {network}")
        except Exception as e:
            logging.exception(f"Ошибка удаления значения blacklist_networks для пользователя {user_id}: {e}")

    async def get_top_blacklist_networks(self, user_id: int, top_n: int = 5) -> list[tuple[str, int]]:
        sql = """
        WITH user_blacklist AS (
            SELECT unnest(blacklist_networks) AS network
            FROM user_inter_exchange_settings
            WHERE user_id = $1
        ),
        all_blacklists AS (
            SELECT unnest(blacklist_networks) AS network
            FROM user_inter_exchange_settings
        )
        SELECT network, COUNT(*) AS frequency
        FROM all_blacklists
        WHERE network NOT IN (SELECT network FROM user_blacklist)
        GROUP BY network
        ORDER BY frequency DESC
        LIMIT $2;
        """
        try:
            top_networks = await self.pool.fetch(sql, user_id, top_n)
            logging.debug(
                f"Получены топ {top_n} сетей из чёрного списка, которых нет у пользователя {user_id}: {top_networks}")
            return [(row['network'], row['frequency']) for row in top_networks]
        except Exception as e:
            logging.exception(f"Ошибка получения топ сетей из черного списка без учёта пользователя {user_id}: {e}")
            return []

    async def add_blacklist_coin_for_exchange(self, user_id: int, coin_for_exchange: str):
        """
        coin_for_exchange: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_coin_for_exchange = array_append(blacklist_coin_for_exchange, $2)
        WHERE user_id = $1 AND NOT ($2 = ANY(blacklist_coin_for_exchange));
        """
        try:
            await self.pool.execute(sql, user_id, coin_for_exchange)
            logging.info(f"Обновлено значение blacklist_coin_for_exchange для пользователя {user_id}: {coin_for_exchange}")
        except Exception as e:
            logging.exception(f"Ошибка обновления значения blacklist_coin_for_exchange для пользователя {user_id}: {e}")

    async def remove_blacklist_coin_for_exchange(self, user_id: int, coin_for_exchange: str):
        """
        coin_for_exchange: str
        """
        sql = f"""
        UPDATE user_inter_exchange_settings
        SET blacklist_coin_for_exchange = array_remove(blacklist_coin_for_exchange, $2)
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, coin_for_exchange)
            logging.info(f"Удалено значение coin_for_exchange для пользователя {user_id}: {coin_for_exchange}")
        except Exception as e:
            logging.exception(f"Ошибка удаления значения coin_for_exchange для пользователя {user_id}: {e}")

    async def get_top_blacklist_coin_for_exchange(self, user_id: int, top_n: int = 5) -> list[tuple[str, int]]:
        sql = """
        WITH user_blacklist AS (
            SELECT unnest(blacklist_coin_for_exchange) AS coin_for_exchange
            FROM user_inter_exchange_settings
            WHERE user_id = $1
        ),
        all_blacklists AS (
            SELECT unnest(blacklist_coin_for_exchange) AS coin_for_exchange
            FROM user_inter_exchange_settings
        )
        SELECT coin_for_exchange, COUNT(*) AS frequency
        FROM all_blacklists
        WHERE coin_for_exchange NOT IN (SELECT coin_for_exchange FROM user_blacklist)
        GROUP BY coin_for_exchange
        ORDER BY frequency DESC
        LIMIT $2;
        """
        try:
            top_coin_for_exchange = await self.pool.fetch(sql, user_id, top_n)
            logging.debug(
                f"Получены топ {top_n} монет к бирже из чёрного списка, которых нет у пользователя {user_id}: {top_coin_for_exchange}")
            return [(row['coin_for_exchange'], row['frequency']) for row in top_coin_for_exchange]
        except Exception as e:
            logging.exception(f"Ошибка получения топ монет к бирже из черного списка без учёта пользователя {user_id}: {e}")
            return []

    async def add_referral(self, user_id: int, referral_id: int):
        """
        Добавляет реферала в базу данных.
        :param user_id: ID пользователя, который пригласил реферала.
        :param referral_id: ID пользователя, который является рефералом.
        """
        sql = """
        INSERT INTO referrals(user_id, referral_id)
        VALUES($1, $2)
        ON CONFLICT (user_id) DO NOTHING;
        """
        try:
            await self.pool.execute(sql, user_id, referral_id)
            logging.info(f"{user_id} пригласил {referral_id}.")
        except Exception as e:
            logging.exception(f"Ошибка при добавлении реферала {user_id} с рефералом {referral_id}: {e}")

    async def get_referrals(self, user_id: int) -> list[int]:
        """
        Получить список referral_id всех пользователей, приглашённых данным user_id.

        :param user_id: ID пригласившего пользователя (реферера)
        :return: Список ID всех его рефералов
        """
        sql = "SELECT referral_id FROM referrals WHERE user_id = $1"
        try:
            rows = await self.pool.fetch(sql, user_id)
            return [row["referral_id"] for row in rows]
        except Exception as e:
            logging.exception(f"Ошибка при получении списка рефералов для user_id={user_id}: {e}")
            return []

    async def check_if_user_already_referred(self, referral_id: int) -> bool:
        """
        Проверить, был ли пользователь уже кем-то приглашён.

        :param referral_id: ID пользователя, которого могли пригласить
        :return: True — если он уже есть в таблице как приглашённый, иначе False
        """
        sql = "SELECT 1 FROM referrals WHERE referral_id = $1"
        try:
            row = await self.pool.fetchrow(sql, referral_id)
            return row is not None
        except Exception as e:
            logging.exception(f"Ошибка при проверке приглашения referral_id={referral_id}: {e}")
            return False

    async def add_referrals_quantity(self, user_id: int, quantity: int = 1):
        """
        Добавляет количество рефералов для пользователя.
        :param user_id: ID пользователя
        :param quantity: Количество рефералов
        """
        sql = """
        UPDATE referrals_info
        SET referrals_quantity = referrals_quantity + $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, quantity)
            logging.info(f"Обновлено количество рефералов для пользователя {user_id}: {quantity}")
        except Exception as e:
            logging.exception(f"Ошибка обновления количества рефералов для пользователя {user_id}: {e}")

    async def is_user_recently_registered(self, user_id: int, datetime: str = "1 minute") -> bool:
        """
        Проверяет, был ли пользователь зарегистрирован менее минуты назад (на уровне SQL).

        :param user_id: ID пользователя
        :param datetime: Время для проверки, по умолчанию "1 minute"
        :return: True — если зарегистрирован < datetime назад, иначе False
        """
        sql = f"""
        SELECT registration_datetime >= NOW() - INTERVAL '{datetime}'
        FROM users
        WHERE id = $1
        """
        try:
            result = await self.pool.fetchval(sql, user_id)
            return bool(result)
        except Exception as e:
            logging.exception(f"Ошибка при SQL-проверке времени регистрации пользователя {user_id}: {e}")
            return False

    async def get_user_referrals_info(self, user_id: int):
        sql = "SELECT * FROM referrals_info WHERE user_id = $1"
        try:
            referrals_info = await self.pool.fetchrow(sql, user_id)
            logging.debug(f"Получена реферальная информация пользователя {user_id}: {referrals_info}")
            return referrals_info
        except Exception as e:
            logging.exception(f"Ошибка получения реферальной информации пользователя: {e}")
            return None

    async def reset_user_referral_balance(self, user_id: int):
        sql = """
        UPDATE referrals_info
        SET balance = 0
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id)
            logging.info(f"Обнулен баланс рефералов для пользователя {user_id}")
        except Exception as e:
            logging.exception(f"Ошибка обнуления баланса рефералов для пользователя {user_id}: {e}")

    async def subtract_from_user_referral_balance(self, user_id: int, amount: float):
        """
        Вычитает указанную сумму из баланса рефералов пользователя.
        :param user_id: ID пользователя
        :param amount: Сумма для вычитания
        """
        sql = """
        UPDATE referrals_info
        SET balance = balance - $2
        WHERE user_id = $1;
        """
        try:
            await self.pool.execute(sql, user_id, amount)
            logging.info(f"Сумма {amount} вычтена из баланса рефералов пользователя {user_id}")
        except Exception as e:
            logging.exception(f"Ошибка при вычитании суммы {amount} из баланса рефералов пользователя {user_id}: {e}")

    async def get_user_from_blacklist(self, user_id: int):
        try:
            sql = """
            SELECT user_id FROM blacklist WHERE user_id = $1;
            """
            return await self.pool.fetchval(sql, user_id)
        except:
            return None

