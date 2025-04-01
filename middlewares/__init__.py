from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware(default_limit=1))
    dp.callback_query.middleware(ThrottlingMiddleware(default_limit=0.5))
