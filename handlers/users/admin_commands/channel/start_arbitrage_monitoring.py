import asyncio
import copy

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.admin import IsMainAdmin
from data.get_files import load_channel_monitoring_available
from services.redis_clients import inter_exchange_redis
from pprint import pprint

from utils.filter_pairs import (recalculate_spread_from_net_profit, filter_significant_pairs_changes,
                                recalculate_and_filter_by_net_profit)

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
                # pprint(all_pairs)
                print(len(all_pairs))
                for pair, data in all_pairs.items():
                    # region ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ

                    coin = data['coin']
                    avg_buy_price = data['avg_buy_price']
                    avg_sell_price = data['avg_sell_price']
                    buy_orders = data['buy_orders']
                    buy_price_range = data['buy_price_range']
                    exchange_buy = data['exchange_buy']
                    exchange_sell = data['exchange_sell']
                    trade_urls = data['trade_urls']
                    first_exchange_coin_confirmations = data['first_exchange_coin_confirmations']
                    first_exchange_coin_contract = data['first_exchange_coin_contract']
                    first_exchange_deposit_withdraw_links = data['first_exchange_deposit_withdraw_links']
                    first_exchange_loan = data['first_exchange_loan']
                    first_exchange_margin = data['first_exchange_margin']
                    futures = data['futures']
                    net_profit = data['net_profit']
                    network = data['network']
                    profit_coin = data['profit_coin']
                    profit_usdt = data['profit_usdt']
                    second_exchange_coin_confirmations = data['second_exchange_coin_confirmations']
                    second_exchange_coin_contract = data['second_exchange_coin_contract']
                    second_exchange_deposit_withdraw_links = data['second_exchange_deposit_withdraw_links']
                    second_exchange_loan = data['second_exchange_loan']
                    second_exchange_margin = data['second_exchange_margin']
                    sell_orders = data['sell_orders']
                    sell_price_range = data['sell_price_range']
                    spot_fee_first_exchange = data['spot_fee_first_exchange']
                    spot_fee_second_exchange = data['spot_fee_second_exchange']
                    spot_percent_fee_first_exchange = data['spot_percent_fee_first_exchange']
                    spot_percent_fee_second_exchange = data['spot_percent_fee_second_exchange']
                    spread = data['spread']
                    total_buy_amount = data['total_buy_amount']
                    total_sell_amount = data['total_sell_amount']
                    volume_coin = data['volume_coin']
                    volume_usdt = data['volume_usdt']
                    withdraw_fee = data['withdraw_fee']

                    # endregion
                    if pair not in prev_pairs:
                        await message.bot.send_message(chat_id="@VazonezArbitrageChannel",
                                                       disable_web_page_preview=True,
                                                       parse_mode="HTML",
                                                       text=f"""Н<b><a href="{data['trade_urls']['buy_link']}">{data['exchange_buy']}</a> -> <a href="{data['trade_urls']['sell_link']}">{data['exchange_sell']}</a></b>

<b>Монета: ${coin} <code>{coin}</code></b>
<b>Сеть: {network}</b>
<b>Чистый профит: {net_profit} USDT</b>
<b>Профит в монете: {profit_coin}</b>
<b>Спред: {round(float(spread), 2)}%</b>


<b><a href="{first_exchange_deposit_withdraw_links['withdraw_link']}">ВЫВОД МОНЕТЫ</a></b>
<b><a href="{second_exchange_deposit_withdraw_links['deposit_link']}">ДЕПОЗИТ МОНЕТЫ</a></b>""")

                    else:
                        await message.bot.send_message(chat_id="@VazonezArbitrageChannel",
                                                       disable_web_page_preview=True,
                                                       parse_mode="HTML",
                                                       text=f"""С<b><a href="{data['trade_urls']['buy_link']}">{data['exchange_buy']}</a> -> <a href="{data['trade_urls']['sell_link']}">{data['exchange_sell']}</a></b>
                    
<b>Монета: ${coin} <code>{coin}</code></b>
<b>Сеть: {network}</b>
<b>Чистый профит: {net_profit} USDT</b>
<b>Профит в монете: {profit_coin}</b>
<b>Спред: {spread}%</b>


<b><a href="{first_exchange_deposit_withdraw_links['withdraw_link']}">ВЫВОД МОНЕТЫ</a></b>
<b><a href="{second_exchange_deposit_withdraw_links['deposit_link']}">ДЕПОЗИТ МОНЕТЫ</a></b>""")
                    await asyncio.sleep(3)
                        # prev_data = prev_pairs[pair]
                        # if data != prev_data:
                        #     await message.bot.send_message(chat_id="@VazonezArbitrageChannel",
                        #                                    text="Связка")
                        #     await asyncio.sleep(10)
                # await message.bot.send_message(chat_id="@VazonezArbitrageChannel",
                #                                text="Связка")

            prev_pairs = raw_pairs_for_prev
            await asyncio.sleep(1)
