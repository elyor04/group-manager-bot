from aiogram import Dispatcher
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from database.models import set_username
from utils.chatmember import is_admin, is_muted, is_banned

mute_cb = CallbackData("mute", "user_id", "action")
ban_cb = CallbackData("ban", "user_id", "action")


async def cancel_mute(callback_query: types.CallbackQuery, callback_data: dict):
    set_username(
        callback_query.message.chat.id,
        callback_query.from_user.id,
        callback_query.from_user.username,
    )

    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user = await callback_query.message.bot.get_chat(int(callback_data["user_id"]))
    set_username(callback_query.message.chat.id, user.id, user.username)

    if not await is_muted(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not muted.")
        return

    chat = await callback_query.message.bot.get_chat(callback_query.message.chat.id)

    await callback_query.message.chat.restrict(
        user_id=user.id,
        permissions=chat.permissions,
    )
    await callback_query.message.edit_text("Mute has been canceled.")


async def cancel_ban(callback_query: types.CallbackQuery, callback_data: dict):
    set_username(
        callback_query.message.chat.id,
        callback_query.from_user.id,
        callback_query.from_user.username,
    )

    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user = callback_query.message.bot.get_chat(int(callback_data["user_id"]))
    set_username(callback_query.message.chat.id, user.id, user.username)

    if not await is_banned(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not banned.")
        return

    await callback_query.message.chat.unban(user_id=user.id)
    await callback_query.message.edit_text("Ban has been canceled.")


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_mute, mute_cb.filter(action="cancel"))
    dp.register_callback_query_handler(cancel_ban, ban_cb.filter(action="cancel"))
