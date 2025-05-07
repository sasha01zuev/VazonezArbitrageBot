import asyncio
import copy
import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import IsMainAdmin
from data.get_files import load_channel_monitoring_available
from services.redis_clients import inter_exchange_redis
from pprint import pprint
from aiogram.exceptions import TelegramRetryAfter
from utils.filter_pairs import (recalculate_spread_from_net_profit, filter_significant_pairs_changes,
                                recalculate_and_filter_by_net_profit, group_and_pack_pairs_into_messages)

admin_channel_router = Router()


@admin_channel_router.message(Command("start_arbitrage_channel_monitoring"), IsMainAdmin())
async def arbitrage_channel_monitoring(message: Message):
    await message.answer("✅ Начинаю мониторинг")
    prev_pairs = {}

    while True:
        is_channel_monitoring_available_data = await load_channel_monitoring_available()
        is_monitoring_available = is_channel_monitoring_available_data['is_available']

        if is_monitoring_available:
            all_pairs_from_redis = await inter_exchange_redis.get_all_pairs()
            raw_pairs_for_prev = copy.deepcopy(all_pairs_from_redis)

            all_pairs = await filter_significant_pairs_changes(current_pairs=all_pairs_from_redis,
                                                               previous_pairs=prev_pairs)
            all_pairs = await recalculate_and_filter_by_net_profit(all_pairs)
            all_pairs = await recalculate_spread_from_net_profit(all_pairs)

            if all_pairs:
                # 🧠 Группируем и упаковываем сообщения
                messages_pairs = await group_and_pack_pairs_into_messages(
                    pairs=all_pairs,
                    previous_pairs=prev_pairs
                )

                logging.info(f"🔹 Подготовлено {len(messages_pairs)} сообщений к отправке")

                try:
                    for i, msg in enumerate(messages_pairs, start=1):
                        logging.info(f"📤 Отправка сообщения {i}/{len(messages_pairs)} ({len(msg)} символов)")
                        # await message.bot.send_message(
                        #     chat_id="@VazonezArbitrageChannel",
                        #     text=msg,
                        #     parse_mode="HTML",
                        #     disable_web_page_preview=True
                        # )
                        await message.bot.send_message(
                            chat_id="-1002666568267",
                            text=msg,
                            parse_mode="HTML",
                            disable_web_page_preview=True
                        )
                        await asyncio.sleep(3)
                except TelegramRetryAfter as e:
                    logging.warning(f"⚠️ FLOOD WARNING: Telegram ограничил рассылку: FloodControl на {e.retry_after} сек")
                    await asyncio.sleep(e.retry_after)
                except Exception as e:
                    logging.error(f"❌ Ошибка при отправке сообщения: {e}")

            prev_pairs = raw_pairs_for_prev
            await asyncio.sleep(1)
