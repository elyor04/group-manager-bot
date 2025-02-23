from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from app.database.utils import get_muted_count, set_muted_count
from app.helpers import is_admin, is_muted, is_banned, extract_args, get_strtime
from app.utils import MuteCallbackData

router = Router()


@router.message(
    Command("mute"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def mute_user(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        message_sender = message.answer

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    if await is_admin(message.chat, user):
        await message.reply("You cannot mute an admin.")
        return

    if await is_muted(message.chat, user):
        await message.reply("User is already muted.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    await message.delete()

    mute_duration = args_dict["timedelta"]
    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""

    if mute_duration:
        await message.chat.restrict(
            user_id=user.id,
            permissions=ChatPermissions(),
            until_date=message.date + mute_duration,
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Cancel Mute",
                        callback_data=MuteCallbackData(user_id=user.id, action="cancel").pack(),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.\nDuration: {get_strtime(mute_duration)}' + reason,
            reply_markup=keyboard,
        )

    else:
        await message.chat.restrict(
            user_id=user.id,
            permissions=ChatPermissions(),
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Cancel Mute",
                        callback_data=MuteCallbackData(user_id=user.id, action="cancel").pack(),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.' + reason,
            reply_markup=keyboard,
        )

    muted_count = await get_muted_count(message.chat.id, user.id)
    await set_muted_count(message.chat.id, user.id, muted_count + 1)
