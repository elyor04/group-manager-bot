from aiogram import Dispatcher, types, F
from utils.chatMember import is_admin, is_muted, is_banned
from utils.callbackData import MuteCallbackData, BanCallbackData


async def cancel_mute(
    callback_query: types.CallbackQuery, callback_data: MuteCallbackData
):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user = await callback_query.message.bot.get_chat(callback_data.user_id)

    if not await is_muted(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not muted.")
        return

    chat = await callback_query.message.bot.get_chat(callback_query.message.chat.id)

    await callback_query.message.chat.restrict(
        user_id=user.id,
        permissions=chat.permissions,
    )
    await callback_query.message.edit_text("Mute has been canceled.")


async def cancel_ban(
    callback_query: types.CallbackQuery, callback_data: BanCallbackData
):
    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user = await callback_query.message.bot.get_chat(callback_data.user_id)

    if not await is_banned(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not banned.")
        return

    await callback_query.message.chat.unban(user_id=user.id)
    await callback_query.message.edit_text("Ban has been canceled.")


def register_callback_handlers(dp: Dispatcher):
    dp.callback_query.register(
        cancel_mute, MuteCallbackData.filter(F.action == "cancel")
    )
    dp.callback_query.register(
        cancel_ban, BanCallbackData.filter(F.action == "cancel")
    )
