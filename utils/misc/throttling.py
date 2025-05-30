from typing import Callable

# Глобальный словарь с лимитами по функциям
THROTTLE_LIMITS = {}


def rate_limit(limit: float = 1.0):
    """
    Декоратор для установки индивидуального лимита на хендлер.
    Работает совместно с ThrottlingMiddleware.
    """
    def decorator(handler: Callable):
        setattr(handler, "rate_limit", limit)
        return handler
    return decorator
