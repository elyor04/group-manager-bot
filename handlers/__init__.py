from pyrogram import Client
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
from .member import register_member_handlers
from .admin import register_admin_handlers
from .check import register_check_handlers


def register_handlers(app: Client):
    register_start_handlers(app)
    register_warn_handlers(app)
    register_mute_handlers(app)
    register_ban_handlers(app)
    register_callback_handlers(app)
    register_unwarn_handlers(app)
    register_unmute_handlers(app)
    register_unban_handlers(app)
    register_info_handlers(app)
    register_write_handlers(app)
    register_delete_handlers(app)
    register_member_handlers(app)
    register_admin_handlers(app)
    register_check_handlers(app)
