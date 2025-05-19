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