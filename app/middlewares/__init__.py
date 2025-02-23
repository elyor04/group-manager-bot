from aiogram import Dispatcher
from .count import CountMiddleware


def register_middlewares(dp: Dispatcher):
    dp.message.middleware(CountMiddleware())
