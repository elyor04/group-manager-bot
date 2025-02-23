from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ChatType
from app.helpers import is_admin, is_muted, is_banned
from app.utils import MuteCallbackData, BanCallbackData

router = Router()


@router.callback_query(
    MuteCallbackData.filter(F.action == "cancel"),
    F.message.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def cancel_mute(callback_query: CallbackQuery, callback_data: MuteCallbackData):
    if not await is_admin(callback_query.message.chat, callback_query.bot):
        await callback_query.answer("Please make me an admin first.")
        return

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


@router.callback_query(
    BanCallbackData.filter(F.action == "cancel"),
    F.message.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def cancel_ban(callback_query: CallbackQuery, callback_data: BanCallbackData):
    if not await is_admin(callback_query.message.chat, callback_query.bot):
        await callback_query.answer("Please make me an admin first.")
        return

    if not await is_admin(callback_query.message.chat, callback_query.from_user):
        await callback_query.answer("You are not an admin of this group.")
        return

    user = await callback_query.message.bot.get_chat(callback_data.user_id)

    if not await is_banned(callback_query.message.chat, user):
        await callback_query.message.edit_text("User is not banned.")
        return

    await callback_query.message.chat.unban(user_id=user.id)
    await callback_query.message.edit_text("Ban has been canceled.")
