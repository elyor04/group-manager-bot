from aiogram import Dispatcher
from .users import register_users_handlers
from .groups import register_groups_handlers


def register_handlers(dp: Dispatcher):
    register_users_handlers(dp)
    register_groups_handlers(dp)
