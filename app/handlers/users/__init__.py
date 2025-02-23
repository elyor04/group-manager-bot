from aiogram import Dispatcher
from . import (
    start,
)


def register_users_handlers(dp: Dispatcher):
    dp.include_routers(
        start.router,
    )
