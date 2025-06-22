import logging

from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import TelegramObject
from services.database.postgresql import Database  # путь от корня
from services.wallets import TRC20Wallet, BEP20Wallet


class RegisterUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logging.debug(f"RegisterUserMiddleware: {event=}, {data=}")

        user = None

        if hasattr(event, "from_user"):
            user = event.from_user

        elif hasattr(event, "message") and hasattr(event.message, "from_user"):
            user = event.message.from_user
        elif hasattr(event, "callback_query") and hasattr(event.callback_query, "from_user"):
            user = event.callback_query.from_user
        elif hasattr(event, "edited_message") and hasattr(event.edited_message, "from_user"):
            user = event.edited_message.from_user
        else:
            logging.warning("User не найден в событии")
            return await handler(event, data)

        db: Database = data["db"]

        if not db:
            logging.critical("База данных не инициализирована в workflow_data")
            return await handler(event, data)

        db_user = await db.get_user(user_id=user.id)
        db_user_subscriptions = await db.get_availability_user_subscriptions(user_id=user.id)
        db_get_user_inter_exchange_exchanges = await db.get_availability_user_inter_exchange_exchanges(user_id=user.id)
        db_get_user_inter_exchange_settings = await db.get_user_inter_exchange_settings(user_id=user.id)
        db_get_user_referral_info = await db.get_user_referral_info(user_id=user.id)
        db_get_user_wallets = await db.get_user_wallets(user_id=user.id)

        if not db_user:
            user_language = "ru" if user.language_code == "ru" else "en"
            await db.add_user(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                language=user_language
            )
            logging.debug(f"User {user.id} зарегистрирован в базу данных.")
        else:
            logging.debug(f"User {user.id} уже был зарегистрирован в базе данных.")

        if not db_user_subscriptions:
            await db.add_user_default_subscriptions(user_id=user.id)
            logging.debug(f"Подписки для пользователя {user.id} добавлены в базу данных.")
        else:
            logging.debug(f"Подписки для пользователя {user.id} уже существуют в базе данных.")

        if not db_get_user_inter_exchange_exchanges:
            await db.add_user_default_inter_exchange_exchanges(user_id=user.id)
            logging.debug(f"Межбиржевые биржи для пользователя {user.id} добавлены в базу данных.")
        else:
            logging.debug(f"Межбиржевые биржи для пользователя {user.id} уже существуют в базе данных.")

        if not db_get_user_inter_exchange_settings:
            await db.add_user_default_inter_exchange_settings(user_id=user.id)
            logging.debug(f"Межбиржевые настройки для пользователя {user.id} добавлены в базу данных.")
        else:
            logging.debug(f"Межбиржевые настройки для пользователя {user.id} уже существуют в базе данных.")

        if not db_get_user_referral_info:
            await db.set_default_user_referral_info(user_id=user.id)
            logging.debug(f"Реферальная информация для пользователя {user.id} добавлена в базу данных.")

        if not db_get_user_wallets:
            trc20_wallet = TRC20Wallet()
            bep20_wallet = BEP20Wallet()

            try:
                trc20_wallet = await trc20_wallet.create_wallet()
                bep20_wallet = await bep20_wallet.create_wallet()
                trc20_address = trc20_wallet['address']
                trc20_key = trc20_wallet['private_key']
                bep20_address = bep20_wallet['address']
                bep20_key = bep20_wallet['private_key']
                logging.debug(f"Кошельки созданы для пользователя {user.id}: "
                              f"TRC20 - {trc20_address}, BEP20 - {bep20_address}\n\n"
                              f"TRC20 Key - {trc20_key}, BEP20 Key - {bep20_key}")
            except Exception as e:
                trc20_address, trc20_key = 'N/A', 'N/A'
                bep20_address, bep20_key = 'N/A', 'N/A'

            wallets = {
                "usdt_bep20_address": bep20_address,
                "usdt_trc20_address": trc20_address,
                "usdt_bep20_key": bep20_key,
                "usdt_trc20_key": trc20_key


            }
            await db.set_default_user_wallets(user_id=user.id, wallets=wallets)
            logging.debug(f"Кошельки для пользователя {user.id} добавлены в базу данных.")
        else:
            logging.debug(f"Кошельки для пользователя {user.id} уже существуют в базе данных.")


        # TODO: В будущем добавить проверку на другие параметры, например на подписку, настройки и т.д.

        return await handler(event, data)
