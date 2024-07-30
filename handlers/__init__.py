from .warn import register_warn_handlers
from .mute import register_mute_handlers
from .ban import register_ban_handlers
from .callbacks import register_callback_handlers


def register_handlers(dp):
    register_warn_handlers(dp)
    register_mute_handlers(dp)
    register_ban_handlers(dp)
    register_callback_handlers(dp)
