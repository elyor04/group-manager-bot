from aiogram import Dispatcher
from . import (
    start,
    chats,
    users,
    count,
)


def register_users_handlers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        chats.router,
        users.router,
        count.router,
    )
