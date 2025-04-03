import logging
from typing import List, Dict
from decimal import Decimal, InvalidOperation


async def recalculate_and_filter_by_net_profit(pairs: dict) -> dict:
    updated_pairs = {}

    for key, data in pairs.items():
        try:
            original_profit = float(data.get("net_profit", 0))
            fee_buy = float(data.get("spot_fee_first_exchange", 0))
            fee_sell = float(data.get("spot_fee_second_exchange", 0))

            clean_profit = original_profit - fee_buy - fee_sell
            if clean_profit > 0:
                data["net_profit"] = round(clean_profit, 2)
                updated_pairs[key] = data

        except Exception as e:
            logging.exception(f"❌ Что-то не так при перерасчёте чистого профита {key}: {e}")
            continue

    return updated_pairs


async def recalculate_spread_from_net_profit(pairs: dict) -> dict:
    """
    Пересчитывает spread для каждой связки как:
    spread = (net_profit / volume_usdt) * 100
    """
    updated_pairs = {}

    for key, data in pairs.items():
        try:
            net_profit = float(data.get("net_profit", 0))
            volume_usdt = float(data.get("volume_usdt", 0))

            if volume_usdt == 0:
                continue  # избегаем деления на 0

            spread = (net_profit / volume_usdt) * 100
            data["spread"] = round(spread, 2)  # можно округлить до нужной точности

            updated_pairs[key] = data

        except (ValueError, TypeError) as e:
            logging.exception(f"❌ Что-то не так с числовыми значениями {key}: {e}")
            continue  # если в данных ошибка — пропускаем связку

    return updated_pairs


async def filter_significant_pairs_changes(current_pairs: dict, previous_pairs: dict) -> dict:
    """
    Возвращает только новые или значительно изменившиеся связки.
    Сравнивает по ключу (exchange1:exchange2:coin).
    """

    def is_significant_change(pair_key: str, prev_data: dict, curr_data: dict) -> bool:
        try:
            prev_profit = float(prev_data.get("net_profit", 0))
            curr_profit = float(curr_data.get("net_profit", 0))
            prev_spread = float(prev_data.get("spread", 0))
            curr_spread = float(curr_data.get("spread", 0))

            profit_diff = curr_profit - prev_profit
            spread_diff = curr_spread - prev_spread

            # Абсолютное изменение профита
            if profit_diff >= 2.0:
                print(f"Предыдущая связка: {prev_data["net_profit"]}\n"
                      f"Текущая связка: {curr_data["net_profit"]}\n")
                print(
                    f"✅ {pair_key} — net_profit изменился: было {prev_profit:.2f} → стало {curr_profit:.2f} "
                    f"(+{profit_diff:.2f} USDT)\n\n")
                return True

            # Относительное изменение профита
            if prev_profit > 0:
                profit_percent_change = (profit_diff / prev_profit) * 100
                if profit_percent_change >= 20:
                    print(f"Предыдущая связка: {prev_data['net_profit']}\n"
                          f"Текущая связка: {curr_data['net_profit']}\n")
                    print(
                        f"✅ {pair_key} — net_profit вырос на {profit_percent_change:.1f}% "
                        f"(было {prev_profit:.2f} → стало {curr_profit:.2f})\n\n")
                    return True

            # Изменение спреда
            if spread_diff >= 0.5:
                print(f"Предыдущая связка: {prev_data['spread']}\n"
                      f"Текущая связка: {curr_data['spread']}\n")
                print(
                    f"✅ {pair_key} — spread изменился: было {prev_spread:.2f}% → стало {curr_spread:.2f}% "
                    f"(+{spread_diff:.2f}%)\n\n")
                return True

            # Если ничего не сработало
            print(
                f"❌ {pair_key} — изменений недостаточно: "
                f"net_profit {prev_profit:.2f} → {curr_profit:.2f} "
                f"(Δ={profit_diff:.2f}), spread {prev_spread:.2f}% → {curr_spread:.2f}% (Δ={spread_diff:.2f}%)"
            )

        except (ValueError, TypeError, ZeroDivisionError) as e:
            print(f"⚠️ Ошибка сравнения пары {pair_key}: {e}")

        return False

    result = {}

    for key, current_data in current_pairs.items():
        previous_data = previous_pairs.get(key)

        if previous_data is None:
            print(f"🆕 Новая связка: {key}")
            result[key] = current_data
        elif is_significant_change(key, previous_data, current_data):
            result[key] = current_data
        # иначе — не добавляем

    return result


async def group_and_pack_pairs_into_messages(pairs: Dict[str, dict], previous_pairs: Dict[str, dict]) -> List[str]:
    """
    Группирует связки по монетам и упаковывает их в сообщения до 4096 символов.
    Новые связки выводятся в приоритет, затем — старые по убыванию профита.
    """
    max_message_length = 4096
    max_messages_per_batch = 10

    def smart_round(value) -> float:
        try:
            num = float(value)

            # Оставляем как есть, если число <= 1 и после точки <= 6 символов
            if num < 1:
                after_dot = str(num).split(".")[1]
                if len(after_dot) <= 6:
                    return num
                # иначе — ищем первые 3 значащих цифры после ведущих нулей
                cleaned = after_dot.lstrip("0")
                return float(f"0.{after_dot[:len(after_dot) - len(cleaned) + 3]}")

            # >=1 и <100 — округляем до 2 знаков
            elif num < 100:
                return round(num, 2)

            # >=100 — округляем до 1 знака
            else:
                return round(num, 1)

        except (ValueError, TypeError, InvalidOperation) as e:
            logging.exception(f"Ошибка преобразования {value} в число: {e}")
            return value

    def format_pair(arbitrage_pair: dict) -> str:
        # region ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ

        coin_name = arbitrage_pair['coin']
        avg_buy_price = smart_round(arbitrage_pair['avg_buy_price'])
        avg_sell_price = smart_round(arbitrage_pair['avg_sell_price'])
        buy_orders = arbitrage_pair['buy_orders']
        buy_price_range = arbitrage_pair['buy_price_range']
        exchange_buy = arbitrage_pair['exchange_buy']
        exchange_sell = arbitrage_pair['exchange_sell']
        trade_urls = arbitrage_pair['trade_urls']
        trade_urls_buy_link = trade_urls['buy_link']
        trade_urls_sell_link = trade_urls['sell_link']
        first_exchange_coin_confirmations = arbitrage_pair['first_exchange_coin_confirmations']
        first_exchange_coin_contract = arbitrage_pair['first_exchange_coin_contract']
        first_exchange_deposit_withdraw_links = arbitrage_pair['first_exchange_deposit_withdraw_links']
        first_exchange_deposit_withdraw_links_withdraw_link = first_exchange_deposit_withdraw_links['withdraw_link']
        first_exchange_loan = arbitrage_pair['first_exchange_loan']
        first_exchange_margin = arbitrage_pair['first_exchange_margin']
        futures = arbitrage_pair['futures']
        net_profit = smart_round(arbitrage_pair['net_profit'])
        network = arbitrage_pair['network']
        profit_coin = smart_round(arbitrage_pair['profit_coin'])
        profit_usdt = arbitrage_pair['profit_usdt']
        second_exchange_coin_confirmations = arbitrage_pair['second_exchange_coin_confirmations']
        second_exchange_coin_contract = arbitrage_pair['second_exchange_coin_contract']
        second_exchange_deposit_withdraw_links = arbitrage_pair['second_exchange_deposit_withdraw_links']
        second_exchange_deposit_withdraw_links_deposit_link = second_exchange_deposit_withdraw_links['deposit_link']
        second_exchange_loan = arbitrage_pair['second_exchange_loan']
        second_exchange_margin = arbitrage_pair['second_exchange_margin']
        sell_orders = arbitrage_pair['sell_orders']
        sell_price_range = arbitrage_pair['sell_price_range']
        spot_fee_first_exchange = smart_round(arbitrage_pair['spot_fee_first_exchange'])
        spot_fee_second_exchange = smart_round(arbitrage_pair['spot_fee_second_exchange'])
        spot_percent_fee_first_exchange = arbitrage_pair['spot_percent_fee_first_exchange']
        spot_percent_fee_second_exchange = arbitrage_pair['spot_percent_fee_second_exchange']
        spread = arbitrage_pair['spread']
        total_buy_amount = smart_round(arbitrage_pair['total_buy_amount'])
        total_sell_amount = smart_round(arbitrage_pair['total_sell_amount'])
        volume_coin = arbitrage_pair['volume_coin']
        volume_usdt = arbitrage_pair['volume_usdt']
        withdraw_fee = smart_round(arbitrage_pair['withdraw_fee'])

        # endregion

        # region ПРОВЕРКА НА СХОЖЕСТЬ КОНТРАКТОВ
        contract_message = ""
        if (first_exchange_coin_contract and second_exchange_coin_contract) and (
                first_exchange_coin_contract.lower() == second_exchange_coin_contract.lower()):
            contract_message = ("<b>✅ Одинаковые контракты</b>\n"
                                f"<blockquote>{first_exchange_coin_contract}</blockquote>\n\n")
        # endregion

        # region ПРОВЕРКА НА ПОДТВЕРЖДЕНИЯ СЕТИ
        confirmations_message = ""
        if second_exchange_coin_confirmations:
            confirmations_message = f"| {second_exchange_coin_confirmations} подтверждений "
        # endregion

        # region ПРОВЕРКА НА ФЬЮЧЕРСЫ
        futures_message = ""
        if futures:
            links = [f"<b><a href='{link}'>{exchange}</a></b>" for exchange, link in futures.items()]
            futures_message = "<b>🛡️ Фьючерсы:</b> " + " | ".join(links)
        # endregion

        message = (f"<b><code>{coin_name}</code> | <a href='{trade_urls_buy_link}'>{exchange_buy}</a> → "
                   f"<a href='{trade_urls_sell_link}'>{exchange_sell}</a></b>\n\n"
                   f""
                   f""
                   f"<b>1️⃣ <a href='{trade_urls_buy_link}'>{exchange_buy}</a> | "
                   f"<a href='{first_exchange_deposit_withdraw_links_withdraw_link}'>Вывод</a></b>\n"
                   f""
                   f"        Средняя цена: <b>{avg_buy_price}$</b>\n"
                   f"        Ордера: <b>{buy_price_range}</b>\n"
                   f"        Объём: <b>{total_buy_amount}$</b>\n\n"
                   f""
                   f""
                   f"<b>2️⃣ <a href='{trade_urls_sell_link}'>{exchange_sell}</a> | "
                   f"<a href='{second_exchange_deposit_withdraw_links_deposit_link}'>Депозит</a></b>\n"
                   f""
                   f"        Средняя цена: <b>{avg_sell_price}$</b>\n"
                   f"        Ордера: <b>{sell_price_range}</b>\n"
                   f"        Объём: <b>{total_sell_amount}$</b>\n\n"
                   f""
                   f""
                   f"{contract_message}"
                   f""
                   f""
                   f"<b>🔗 Сеть:</b> {network} {confirmations_message}\n"
                   f"<b>💵 Чистый профит:</b> {net_profit}$ | {profit_coin} ${coin_name}\n"
                   f"<b>📊 Spread:</b> {spread}%\n"
                   f"<b>✂️ Комиссии:</b> <b>B</b> — {spot_fee_first_exchange}$, <b>S</b> — {spot_fee_second_exchange}$, "
                   f"<b>W</b> — {withdraw_fee}$\n\n"
                   f""
                   f"{futures_message}"
                   f""
                   f"\n\n\n")

        return message

    # 1. Разделение на новые и старые
    new_pairs = {k: v for k, v in pairs.items() if k not in previous_pairs}
    old_pairs = {k: v for k, v in pairs.items() if k in previous_pairs}

    # 2. Объединение: новые (вверх) + старые (сортировка по net_profit ↓)
    sorted_pairs = {
        **{k: new_pairs[k] for k in sorted(new_pairs, key=lambda x: float(new_pairs[x].get("net_profit", 0)), reverse=True)},
        **{k: old_pairs[k] for k in sorted(old_pairs, key=lambda x: float(old_pairs[x].get("net_profit", 0)), reverse=True)}
    }

    # 3. Группировка по монетам
    grouped_by_coin = {}
    for key, pair in sorted_pairs.items():
        coin = pair.get("coin")
        if coin not in grouped_by_coin:
            grouped_by_coin[coin] = []
        grouped_by_coin[coin].append(pair)

    # 4. Упаковка в сообщения
    final_messages = []
    for coin, coin_pairs in grouped_by_coin.items():
        current_message = ""
        for pair in coin_pairs:
            formatted = format_pair(pair)
            if len(current_message) + len(formatted) <= max_message_length:
                current_message += formatted
            else:
                final_messages.append(current_message.strip())
                current_message = formatted

        if current_message.strip():
            final_messages.append(current_message.strip())

    return final_messages[:max_messages_per_batch]
