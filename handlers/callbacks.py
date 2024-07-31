from aiogram import Dispatcher
from aiogram import types
from aiogram.types import ChatPermissions
from aiogram.utils.callback_data import CallbackData
from utils.admin import is_admin

mute_cb = CallbackData("mute", "user_id", "action")
ban_cb = CallbackData("ban", "user_id", "action")


async def cancel_mute(callback_query: types.CallbackQuery, callback_data: dict):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user_id = int(callback_data["user_id"])
    await callback_query.message.chat.restrict(
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=True),
    )
    await callback_query.message.edit_text("Mute has been canceled.")


async def cancel_ban(callback_query: types.CallbackQuery, callback_data: dict):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user_id = int(callback_data["user_id"])
    await callback_query.message.chat.unban(user_id=user_id)
    await callback_query.message.edit_text("Ban has been canceled.")


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_mute, mute_cb.filter(action="cancel"))
    dp.register_callback_query_handler(cancel_ban, ban_cb.filter(action="cancel"))
