from services.redis_manager import RedisArbitrageManager


# Создаём два Redis менеджера
inter_exchange_redis = RedisArbitrageManager(db=0)
# futures_redis = RedisArbitrageManager(db=1)  # Если это другая база в redis например для фьючерсов