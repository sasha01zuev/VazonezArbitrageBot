# middlewares/__init__.py
from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.message.outer_middleware(ThrottlingMiddleware(limit=1))
    dp.callback_query.outer_middleware(ThrottlingMiddleware(limit=0.5))
