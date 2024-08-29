from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from utils.callbackData import CallbackData
from utils.chatMember import is_admin, is_muted, is_banned

mute_cb = CallbackData("mute", "user_id", "action")
ban_cb = CallbackData("ban", "user_id", "action")


async def cancel_mute(client: Client, callback_query: types.CallbackQuery):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    callback_data = mute_cb.parse(callback_query.data)
    user = await client.get_chat(int(callback_data["user_id"]))

    if not await is_muted(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not muted.")
        return

    chat = await client.get_chat(callback_query.message.chat.id)

    await callback_query.message.chat.restrict_member(
        user_id=user.id,
        permissions=chat.permissions,
    )
    await callback_query.message.edit_text("Mute has been canceled.")


async def cancel_ban(client: Client, callback_query: types.CallbackQuery):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    callback_data = ban_cb.parse(callback_query.data)
    user = await client.get_chat(int(callback_data["user_id"]))

    if not await is_banned(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not banned.")
        return

    await callback_query.message.chat.unban_member(user_id=user.id)
    await callback_query.message.edit_text("Ban has been canceled.")


def register_callback_handlers(dp: Dispatcher):
    dp.add_handler(
        CallbackQueryHandler(
            cancel_mute, mute_cb.filter(action="cancel") & filters.group
        ),
        0,
    )
    dp.add_handler(
        CallbackQueryHandler(
            cancel_ban, ban_cb.filter(action="cancel") & filters.group
        ),
        0,
    )
