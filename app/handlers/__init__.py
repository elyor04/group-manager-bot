from aiogram import Dispatcher
from .start import register_start_handlers
from .warn import register_warn_handlers
from .mute import register_mute_handlers
from .ban import register_ban_handlers
from .callbacks import register_callback_handlers
from .unwarn import register_unwarn_handlers
from .unmute import register_unmute_handlers
from .unban import register_unban_handlers
from .info import register_info_handlers
from .write import register_write_handlers
from .delete import register_delete_handlers
from .silence import register_silence_handlers
from .unsilence import register_unsilence_handlers
from .member import register_member_handlers
from .admin import register_admin_handlers
from .check import register_check_handlers
from .count import register_count_handlers


def register_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_warn_handlers(dp)
    register_mute_handlers(dp)
    register_ban_handlers(dp)
    register_callback_handlers(dp)
    register_unwarn_handlers(dp)
    register_unmute_handlers(dp)
    register_unban_handlers(dp)
    register_info_handlers(dp)
    register_write_handlers(dp)
    register_delete_handlers(dp)
    register_silence_handlers(dp)
    register_unsilence_handlers(dp)
    register_member_handlers(dp)
    register_admin_handlers(dp)
    register_check_handlers(dp)
    register_count_handlers(dp)
