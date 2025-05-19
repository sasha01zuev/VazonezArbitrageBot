from aiogram import Dispatcher
from .debug_logger import DebugLoggerMiddleware
from .throttling import ThrottlingMiddleware
from .register_user_into_db import RegisterUserMiddleware


def setup(dp: Dispatcher):
    dp.message.middleware(DebugLoggerMiddleware())
    dp.callback_query.middleware(DebugLoggerMiddleware())
    dp.inline_query.middleware(DebugLoggerMiddleware())
    dp.edited_message.middleware(DebugLoggerMiddleware())

    dp.message.middleware(ThrottlingMiddleware(default_limit=1))
    dp.callback_query.middleware(ThrottlingMiddleware(default_limit=0.5))

    dp.update.middleware(RegisterUserMiddleware())
