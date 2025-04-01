import logging


async def filter_negative_profit_pairs(pairs: dict) -> dict:
    filtered = {}
    for key, data in pairs.items():
        try:
            profit = float(data.get("net_profit", 0))
            fee_buy = float(data.get("spot_fee_first_exchange", 0))
            fee_sell = float(data.get("spot_fee_second_exchange", 0))
            net = profit - fee_buy - fee_sell

            if net > 0:
                filtered[key] = data
        except Exception as e:
            logging.exception(f"❌ Ошибка при разборе {key}: {e}")
            continue
    return filtered


async def recalculate_net_profit_with_spot_fees(pairs: dict) -> dict:
    """
    Для каждой связки пересчитывает net_profit с учётом комиссии спота на покупку и продажу:
    net_profit = net_profit - spot_fee_first_exchange - spot_fee_second_exchange
    """
    updated_pairs = {}

    for key, data in pairs.items():
        try:
            net_profit = float(data.get("net_profit", 0))
            fee_buy = float(data.get("spot_fee_first_exchange", 0))
            fee_sell = float(data.get("spot_fee_second_exchange", 0))

            # Пересчитываем net_profit
            net_profit_adjusted = net_profit - fee_buy - fee_sell

            if net_profit_adjusted <= 0:
                logging.info(f"❌ {key} имеет отрицательный net_profit: {net_profit_adjusted}")
                continue
            # Обновляем значение в связке
            data["net_profit"] = round(net_profit_adjusted, 2)  # округление по желанию
            updated_pairs[key] = data

        except (ValueError, TypeError) as e:
            logging.exception(f"❌ Что-то не так с числовыми значениями {key}: {e}")
            # Если какие-то поля некорректные — просто пропускаем связку
            continue

    return updated_pairs
