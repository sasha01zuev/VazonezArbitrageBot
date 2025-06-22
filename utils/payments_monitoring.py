import asyncio
import json
import logging
from datetime import datetime

from marshmallow import missing

from config.config import MAIN_ADMIN
from keyboards.inline import subscriptions_monitoring_keyboard, get_back_keyboard
from services.database.postgresql import Database
from services.wallets.usdt_wallet import TRC20Wallet, BEP20Wallet
from aiogram import Bot

from utils.i18n import TextProxy
from utils.texts import TEXTS


async def monitor_pending_wallets(bot: Bot, db: Database, interval: int = 30):
    """
    Циклическая проверка кошельков с неистекшим временем оплаты.
    """
    trc20_wallet = TRC20Wallet()
    bep20_wallet = BEP20Wallet()

    base_interval = interval  # сохраняем исходный "базовый" интервал

    while True:
        try:

            all_monitoring_wallets = await db.get_all_monitoring_wallets()
            logging.debug(f"Получены кошельки для мониторинга: {all_monitoring_wallets}")

            if len(all_monitoring_wallets) <= 2:
                current_interval = 10
            elif len(all_monitoring_wallets) <= 5:
                current_interval = 5
            elif len(all_monitoring_wallets) <= 10:
                current_interval = 3
            elif len(all_monitoring_wallets) <= 20:
                current_interval = 2
            elif len(all_monitoring_wallets) <= 30:
                current_interval = 1
            elif len(all_monitoring_wallets) <= 60:
                current_interval = 0.5
            else:
                current_interval = 0.3

            logging.debug(f"Текущий интервал проверки: {current_interval} секунд.")

            # region Получаем все кошельки с истекшим временем оплаты и отправляем уведомления
            expired_wallets = await db.get_all_expired_wallets()

            for wallet in expired_wallets:
                user_id = wallet['user_id']
                usdt_bep20_address = wallet['usdt_bep20_address']
                usdt_trc20_address = wallet['usdt_trc20_address']
                usdt_bep20_key = wallet['usdt_bep20_key']
                usdt_trc20_key = wallet['usdt_trc20_key']
                created_at = wallet['created_at']
                expired_at = wallet['expires_at']
                subscription_price = wallet['subscription_price']
                arbitrage_type = wallet['arbitrage_type']
                subscription_type = wallet['subscription_type']
                time_reminder = wallet['time_reminder']
                payment_status = wallet['payment_status']

                if isinstance(time_reminder, str):
                    time_reminder = json.loads(time_reminder)
                if isinstance(payment_status, str):
                    payment_status = json.loads(payment_status)

                time_reminder_expired = time_reminder.get('expired', False)

                if not time_reminder_expired:
                    time_reminder = {
                        "15_minutes": False,
                        "10_minutes": False,
                        "5_minutes": False,
                        "3_minutes": False,
                        "1_minutes": False,
                        "0_minutes": False,
                        "expired": True
                    }
                    payment_status = {
                        "pending_confirmation": False,
                        "confirmed": False,
                        "insufficient": False
                    }

                    await db.reset_user_wallets_in_monitoring(user_id=user_id, usdt_bep_20_address=usdt_bep20_address,
                                                              usdt_bep_20_key=usdt_bep20_key,
                                                              usdt_trc_20_address=usdt_trc20_address,
                                                              usdt_trc_20_key=usdt_trc20_key,
                                                              time_reminder=time_reminder,
                                                              payment_status=payment_status)

                    user_data = await db.get_user(user_id)
                    lang = user_data.get("language", "ru") if user_data else "ru"
                    texts = TextProxy(TEXTS, lang=lang)

                    await bot.send_message(
                        chat_id=user_id,
                        text=texts.commands.subscriptions_monitoring.notifications.time_reminder.payment_time_expired,
                        disable_web_page_preview=True, parse_mode="HTML"
                    )

                    await asyncio.sleep(current_interval)
            # endregion

            # Выбор текущего интервала в зависимости от ситуации
            if not all_monitoring_wallets:
                current_interval = base_interval
                logging.debug(
                    f"Нет кошельков для мониторинга. Устанавливаем интервал {current_interval} секунд.")
                await asyncio.sleep(current_interval)
                continue

            for wallet in all_monitoring_wallets:
                user_id = wallet['user_id']
                usdt_bep20_address = wallet['usdt_bep20_address']
                usdt_trc20_address = wallet['usdt_trc20_address']
                usdt_bep20_key = wallet['usdt_bep20_key']
                usdt_trc20_key = wallet['usdt_trc20_key']
                created_at = wallet['created_at']
                expired_at = wallet['expires_at']
                subscription_price = wallet['subscription_price']
                arbitrage_type = wallet['arbitrage_type']
                subscription_type = wallet['subscription_type']
                time_reminder = wallet['time_reminder']
                payment_status = wallet['payment_status']

                if isinstance(time_reminder, str):
                    time_reminder = json.loads(time_reminder)

                if isinstance(payment_status, str):
                    payment_status = json.loads(payment_status)

                user_data = await db.get_user(user_id)

                if user_data and "language" in user_data:
                    lang = user_data["language"]
                    logging.debug(f"Пользователь {user_id} язык: {lang}")
                else:
                    # Если язык не найден, можно установить язык по умолчанию
                    lang = "ru"
                    logging.debug(f"Пользователь {user_id} язык по умолчанию: {lang}")

                texts = TextProxy(TEXTS, lang=lang)

                logging.debug(f"\n"
                              f"user_id: {user_id}\n"
                              f"usdt_bep20_address: {usdt_bep20_address} type: {type(usdt_bep20_address)}\n"
                              f"usdt_trc20_address: {usdt_trc20_address} type: {type(usdt_trc20_address)}\n"
                              f"usdt_bep20_key: {usdt_bep20_key} type: {type(usdt_bep20_key)}\n"
                              f"usdt_trc20_key: {usdt_trc20_key} type: {type(usdt_trc20_key)}\n"
                              f"created_at: {created_at} type: {type(created_at)}\n"
                              f"expired_at: {expired_at} type: {type(expired_at)}\n"
                              f"subscription_price: {subscription_price} type: {type(subscription_price)}\n"
                              f"arbitrage_type: {arbitrage_type} type: {type(arbitrage_type)}\n"
                              f"subscription_type: {subscription_type} type: {type(subscription_type)}\n"
                              f"time_reminder: {time_reminder} type: {type(time_reminder)}\n"
                              f"payment_status: {payment_status} type: {type(payment_status)}\n")

                time_reminder_expired = time_reminder.get('expired', True)

                # region ПРОВЕРКА СТАТУСА ПЛАТЕЖА
                payment_usdt_trc20_status = None
                payment_usdt_bep20_status = None
                usdt_trc20_balance = None
                usdt_bep20_balance = None

                if not payment_status['pending_confirmation']:
                    try:
                        payment_usdt_trc20_status = await trc20_wallet.check_payment(
                            address=usdt_trc20_address, subscription_price=float(subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке платежа TRC20 для пользователя {user_id}: {e}")
                        payment_usdt_trc20_status = {'status': 'error', 'message': str(e)}
                    try:
                        payment_usdt_bep20_status = await bep20_wallet.check_payment(
                            address=usdt_bep20_address, subscription_price=float(subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке платежа BEP20 для пользователя {user_id}: {e}")
                        payment_usdt_bep20_status = {'status': 'error', 'message': str(e)}

                    logging.debug(f"\n"
                                  f"Проверка статуса платежа для пользователя {user_id}:\n"
                                  f"TRC20: {payment_usdt_trc20_status}\n"
                                  f"BEP20: {payment_usdt_bep20_status}")
                elif not payment_status['insufficient']:
                    try:
                        payment_usdt_trc20_status = await trc20_wallet.is_transaction_confirmed(
                            address=usdt_trc20_address, subscription_price=float(subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке платежа TRC20 для пользователя {user_id}: {e}")
                        payment_usdt_trc20_status = {'status': 'error', 'message': str(e)}
                    try:
                        payment_usdt_bep20_status = await bep20_wallet.check_payment(
                            address=usdt_bep20_address, subscription_price=float(subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке платежа BEP20 для пользователя {user_id}: {e}")
                        payment_usdt_bep20_status = {'status': 'error', 'message': str(e)}

                    logging.debug(f"\n"
                                  f"Проверка статуса платежа в режиме ОБНАРУЖЕННОЙ НЕ ПОДТВЕРЖДЕННОЙ ОПЛАТЫ для пользователя {user_id}:\n"
                                  f"TRC20: {payment_usdt_trc20_status}\n"
                                  f"BEP20: {payment_usdt_bep20_status}")
                elif payment_status['insufficient']:
                    try:
                        usdt_trc20_balance = await trc20_wallet.get_balance(address=usdt_trc20_address,
                                                                            subscription_price=float(
                                                                                subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке баланса кошелька TRC20 для пользователя {user_id}: {e}")
                        usdt_trc20_balance = {'status': 'error', 'message': str(e)}

                    try:
                        usdt_bep20_balance = await bep20_wallet.get_balance(address=usdt_bep20_address,
                                                                            subscription_price=float(
                                                                                subscription_price))
                    except Exception as e:
                        logging.error(f"Ошибка при проверке баланса кошелька BEP20 для пользователя {user_id}: {e}")
                        usdt_bep20_balance = {'status': 'error', 'message': str(e)}

                    logging.debug(f"\n"
                                  f"Проверка баланса кошелька в режиме ПОДТВЕРЖДЕННОЙ НЕ ДОСТАТОЧНОЙ ОПЛАТЫ для пользователя {user_id}:\n"
                                  f"TRC20: {usdt_trc20_balance}\n"
                                  f"BEP20: {usdt_bep20_balance}")

                # region ОПЛАТА В TRC20 ПОДТВЕРЖДЕНА НО СУММА ОПЛАТЫ НЕДОСТАТОЧНА. ПРОВЕРКА ОБЩЕГО БАЛАНСА КОШЕЛЬКА
                if usdt_trc20_balance and usdt_trc20_balance['status'] == 'success':
                    current_usdt_trc20_balance, current_trx_balance = usdt_trc20_balance['current_balance']

                    new_wallet = await trc20_wallet.create_wallet()
                    trc20_address = new_wallet['address']
                    trc20_key = new_wallet['private_key']

                    time_reminder = {
                        "15_minutes": False,
                        "10_minutes": False,
                        "5_minutes": False,
                        "3_minutes": False,
                        "1_minutes": False,
                        "0_minutes": False,
                        "expired": True
                    }
                    payment_status = {
                        "pending_confirmation": False,
                        "confirmed": False,
                        "insufficient": False
                    }

                    await db.reset_user_wallets_in_monitoring(user_id=user_id, usdt_bep_20_address=usdt_bep20_address,
                                                              usdt_bep_20_key=usdt_bep20_key,
                                                              usdt_trc_20_address=trc20_address,
                                                              usdt_trc_20_key=trc20_key,
                                                              time_reminder=time_reminder,
                                                              payment_status=payment_status)

                    arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" else "Unknown"
                    subscription_type_message = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
                        texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                            texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                                texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

                    subscription_time = "1 week" if subscription_type == 'one_week' else \
                        "1 month" if subscription_type == 'one_month' else \
                            "3 month" if subscription_type == 'three_month' else \
                                "999 year"

                    await db.add_user_subscription(user_id=user_id, arbitrage_type=arbitrage_type,
                                                   subscription_time=subscription_time)
                    await bot.send_message(
                        chat_id=user_id,
                        text=texts.commands.subscriptions_monitoring.notifications.payment_success_trc20.format(
                            current_usdt_trc20_balance=current_usdt_trc20_balance,
                            arbitrage_type_message=arbitrage_type_message,
                            subscription_type_message=subscription_type_message
                        ),
                        disable_web_page_preview=True, parse_mode="HTML",
                        reply_markup=get_back_keyboard(texts=texts)
                    )

                    await bot.send_message(
                        chat_id=MAIN_ADMIN,
                        text=f"Платеж для пользователя {user_id} в TRC20 успешно подтвержден\n\n"
                             f"Адрес TRC20: <code>{usdt_trc20_address}</code>\n"
                             f"Ключ TRC20: <code>{usdt_trc20_key}</code>\n\n"
                             f"Текущий баланс TRC20: {current_usdt_trc20_balance}\n"
                             f"Текущий баланс TRX: {current_trx_balance}\n"
                             f"Сумма подписки: {subscription_price}\n"
                             f"Арбитражный тип: {arbitrage_type}\n"
                             f"Тип подписки: {subscription_type}",
                        disable_web_page_preview=True, parse_mode="HTML"
                    )
                    await asyncio.sleep(current_interval)
                    continue
                # endregion

                # region ОПЛАТА В TRC20 ПОДТВЕРЖДЕНА И СУММА ОПЛАТЫ ДОСТАТОЧНА
                if payment_usdt_trc20_status and payment_usdt_trc20_status['status'] == 'success':
                    logging.debug(f"Платеж для пользователя {user_id} в TRC20 успешно подтвержден.")
                    payment_amount = payment_usdt_trc20_status['amount']

                    new_wallet = await trc20_wallet.create_wallet()
                    trc20_address = new_wallet['address']
                    trc20_key = new_wallet['private_key']

                    time_reminder = {
                        "15_minutes": False,
                        "10_minutes": False,
                        "5_minutes": False,
                        "3_minutes": False,
                        "1_minutes": False,
                        "0_minutes": False,
                        "expired": True
                    }
                    payment_status = {
                        "pending_confirmation": False,
                        "confirmed": True,
                        "insufficient": False
                    }

                    await db.reset_user_wallets_in_monitoring(user_id=user_id, usdt_bep_20_address=usdt_bep20_address,
                                                              usdt_bep_20_key=usdt_bep20_key,
                                                              usdt_trc_20_address=trc20_address,
                                                              usdt_trc_20_key=trc20_key,
                                                              time_reminder=time_reminder,
                                                              payment_status=payment_status)

                    subscription_time = "1 week" if subscription_type == 'one_week' else \
                        "1 month" if subscription_type == 'one_month' else \
                            "3 month" if subscription_type == 'three_month' else \
                                "999 year"
                    await db.add_user_subscription(user_id=user_id, arbitrage_type=arbitrage_type,
                                                   subscription_time=subscription_time)

                    arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" else "Unknown"
                    subscription_type_message = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
                        texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                            texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                                texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

                    await bot.send_message(
                        chat_id=user_id,
                        text=texts.commands.subscriptions_monitoring.notifications.payment_success_trc20.format(
                            current_usdt_trc20_balance=payment_amount,
                            arbitrage_type_message=arbitrage_type_message,
                            subscription_type_message=subscription_type_message
                        ),
                        disable_web_page_preview=True, parse_mode="HTML",
                        reply_markup=get_back_keyboard(texts=texts)
                    )
                    await bot.send_message(
                        chat_id=MAIN_ADMIN,
                        text=f"Платеж для пользователя {user_id} в TRC20 успешно подтвержден\n\n"
                             f"Адрес TRC20: <code>{usdt_trc20_address}</code>\n"
                             f"Ключ TRC20: <code>{usdt_trc20_key}</code>\n\n"
                             f"Сумма оплаты: {payment_amount}\n"
                             f"Сумма подписки: {subscription_price}\n"
                             f"Арбитражный тип: {arbitrage_type}\n"
                             f"Тип подписки: {subscription_type}",
                        disable_web_page_preview=True, parse_mode="HTML"
                    )
                    await asyncio.sleep(current_interval)
                    continue

                # endregion

                # region ОПЛАТА В TRC20 ПОДТВЕРЖДЕНА НО СУММА ОПЛАТЫ НЕДОСТАТОЧНА
                if payment_usdt_trc20_status and payment_usdt_trc20_status['status'] == 'insufficient':
                    logging.debug(f"Платеж для пользователя {user_id} в TRC20 подтвержден, но сумма недостаточна.")
                    missing_amount = round(float(payment_usdt_trc20_status['missing']), 2)
                    paid_amount = round(float(payment_usdt_trc20_status['amount']), 2)
                    if not payment_status['insufficient']:
                        available_wallet_time = await db.get_user_available_time_wallet(user_id)
                        available_minutes, available_seconds = available_wallet_time

                        payment_status['insufficient'] = True
                        await db.update_payment_status(user_id, payment_status)

                        await bot.send_message(
                            chat_id=user_id,
                            text=texts.commands.subscriptions_monitoring.notifications.insufficient_trc20.format(
                                usdt_trc20_address=usdt_trc20_address,
                                missing_amount=missing_amount + 0.5,  # Добавляем 0.5 для округления
                                paid_amount=paid_amount,
                                subscription_price=subscription_price,
                                available_minutes=available_minutes,
                                available_seconds=available_seconds,
                            ),
                            disable_web_page_preview=True, parse_mode="HTML")

                        await bot.send_message(
                            chat_id=MAIN_ADMIN,
                            text=f"Платеж для пользователя {user_id} в TRC20 подтвержден, но сумма недостаточна.\n\n"
                                 f"Адрес TRC20: <code>{usdt_trc20_address}</code>\n"
                                 f"Ключ TRC20: <code>{usdt_trc20_key}</code>\n"
                                 f"Недостаточная сумма: {missing_amount}\n"
                                 f"Оплаченная сумма: {paid_amount}\n"
                                 f"Сумма подписки: {subscription_price}",
                            disable_web_page_preview=True, parse_mode="HTML"
                        )

                    await asyncio.sleep(current_interval)
                    continue
                # endregion

                # region ОПЛАТА В TRC20 ОБНАРУЖЕНА
                if payment_usdt_trc20_status and payment_usdt_trc20_status['status'] == 'pending_confirmation':
                    logging.debug(f"Платеж для пользователя {user_id} в ожидании подтверждения.")
                    if not payment_status['pending_confirmation']:
                        await bot.send_message(
                            chat_id=user_id,
                            text=texts.commands.subscriptions_monitoring.notifications.pending_confirmation_trc20.format(
                                transaction_hash=payment_usdt_trc20_status.get('tx_hash', 'Unknown'),
                                amount=payment_usdt_trc20_status.get('amount', 'Unknown')
                            ),
                            disable_web_page_preview=True, parse_mode="HTML")

                        await bot.send_message(
                            chat_id=MAIN_ADMIN,
                            text=f"Платеж для пользователя {user_id} в ожидании подтверждения.\n"
                                 f"Транзакция: {payment_usdt_trc20_status.get('tx_hash', 'Unknown')}\n"
                                 f"Сумма: {payment_usdt_trc20_status.get('amount', 'Unknown')}\n\n"
                                 f"Адрес TRC20: <code>{usdt_trc20_address}</code>\n"
                                 f"Ключ TRC20: <code>{usdt_trc20_key}</code>\n\n"
                                 f"Сумма подписки: {subscription_price}",
                            disable_web_page_preview=True, parse_mode="HTML"
                        )
                        payment_status['pending_confirmation'] = True
                        await db.update_payment_status(user_id, payment_status)

                    await asyncio.sleep(current_interval)
                    continue
                # endregion

                # endregion

                # region УВЕДОМЛЕНИЕ ОБ ИСТЕКАЮЩЕМ ВРЕМЕНИ ОПЛАТЫ

                reminder_thresholds = [15, 10, 5, 3, 1, 0]
                get_user_available_time_wallet = await db.get_user_available_time_wallet(user_id)

                if get_user_available_time_wallet and not time_reminder_expired:  # Проверяем, что время не истекло
                    minutes_left, seconds_left = get_user_available_time_wallet

                    for threshold in reminder_thresholds:
                        field_name = f"{threshold}_minutes"

                        if (field_name in time_reminder and not time_reminder[field_name]
                                and minutes_left <= threshold - 1):
                            time_reminder[field_name] = True
                            await db.update_time_reminder(user_id, time_reminder)

                            arbitrage_type_message = texts.keyboard.arbitrage.buttons.inter_exchange if arbitrage_type == "inter_exchange" \
                                else "Unknown"

                            subscription_type = texts.keyboard.subscriptions.inter_exchange.buttons.one_week if subscription_type == 'one_week' else \
                                texts.keyboard.subscriptions.inter_exchange.buttons.one_month if subscription_type == 'one_month' else \
                                    texts.keyboard.subscriptions.inter_exchange.buttons.three_month if subscription_type == 'three_month' else \
                                        texts.keyboard.subscriptions.inter_exchange.buttons.lifetime

                            await bot.send_message(
                                chat_id=user_id,
                                text=texts.commands.subscriptions_monitoring.notifications.time_reminder.payment_pending.format(
                                    minutes_left=threshold,
                                    arbitrage_type=arbitrage_type_message,
                                    subscription_type=subscription_type,
                                    subscription_price=subscription_price,
                                    usdt_bep20_address=usdt_bep20_address,
                                    usdt_trc20_address=usdt_trc20_address
                                ),
                                disable_web_page_preview=True, parse_mode="HTML",
                                reply_markup=subscriptions_monitoring_keyboard(texts=texts)
                            )
                            break
                else:
                    time_reminder['expired'] = True
                    await db.update_time_reminder(user_id, time_reminder)

                    # Время на оплату вышло
                    await bot.send_message(
                        chat_id=user_id,
                        text=texts.commands.subscriptions_monitoring.notifications.time_reminder.payment_time_expired,
                        disable_web_page_preview=True, parse_mode="HTML"
                    )
                    break
                # endregion

                await asyncio.sleep(current_interval)

        except Exception as e:
            logging.error(f"Ошибка в мониторинге кошельков: {e}")
