from aiogram import Dispatcher
from .warn import register_warn_handlers
from .mute import register_mute_handlers
from .ban import register_ban_handlers
from .callbacks import register_callback_handlers
from .unmute import register_unmute_handlers
from .unban import register_unban_handlers
from .info import register_info_handlers
from .check import register_check_handlers


def register_handlers(dp: Dispatcher):
    register_warn_handlers(dp)
    register_mute_handlers(dp)
    register_ban_handlers(dp)
    register_callback_handlers(dp)
    register_unmute_handlers(dp)
    register_unban_handlers(dp)
    register_info_handlers(dp)
    register_check_handlers(dp)
