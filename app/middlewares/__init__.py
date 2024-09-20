from aiogram import Dispatcher
from .count import register_count_middlewares


def register_middlewares(dp: Dispatcher):
    register_count_middlewares(dp)
