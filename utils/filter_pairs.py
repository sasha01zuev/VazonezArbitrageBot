import logging
from typing import List, Dict


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

    def format_pair(arbitrage_pair: dict) -> str:
        return (
            f"<b>{arbitrage_pair['exchange_buy']} → {arbitrage_pair['exchange_sell']}</b>\n"
            f"<b>Профит:</b> {arbitrage_pair['net_profit']} USDT\n"
            f"<b>Спред:</b> {arbitrage_pair['spread']}%</b>\n"
            f"<b>Сеть:</b> {arbitrage_pair['network']}\n"
            f"<b><a href=\"{arbitrage_pair['first_exchange_deposit_withdraw_links']['withdraw_link']}\">Вывод</a></b> | "
            f"<b><a href=\"{arbitrage_pair['second_exchange_deposit_withdraw_links']['deposit_link']}\">Депозит</a></b>\n\n"
        )

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
        current_message = f"<b>🔹 ARBITRAGE: {coin}</b>\n\n"
        for pair in coin_pairs:
            formatted = format_pair(pair)
            if len(current_message) + len(formatted) <= max_message_length:
                current_message += formatted
            else:
                final_messages.append(current_message.strip())
                current_message = f"<b>🔹 ARBITRAGE: {coin}</b>\n\n{formatted}"

        if current_message.strip():
            final_messages.append(current_message.strip())

    return final_messages[:max_messages_per_batch]
