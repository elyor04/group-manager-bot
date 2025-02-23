from aiogram import Dispatcher
from . import (
    warn,
    mute,
    ban,
    callbacks,
    unwarn,
    unmute,
    unban,
    info,
    write,
    delete,
    welcome,
    admin,
    check,
    count,
)


def register_groups_handlers(dp: Dispatcher):
    dp.include_routers(
        warn.router,
        mute.router,
        ban.router,
        callbacks.router,
        unwarn.router,
        unmute.router,
        unban.router,
        info.router,
        write.router,
        delete.router,
        welcome.router,
        admin.router,
        check.router,
        count.router,
    )
