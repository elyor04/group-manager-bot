from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import (
    get_warning_count,
    set_warning_count,
    get_muted_count,
    set_muted_count,
)
from utils.chatMember import is_admin, is_muted, is_banned
from utils.extractArgs import extract_args, get_strtime
from .callbacks import mute_cb
from datetime import timedelta

mute_durations = {
    3: timedelta(hours=1),
    4: timedelta(days=1),
}


async def warn_user(client: Client, message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["username"]:
        user = await client.get_chat(args_dict["username"])
        message_sender = message.reply

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    if await is_admin(message.chat, user):
        await message.reply("You cannot warn an admin.")
        return

    if await is_muted(message.chat, user):
        await message.reply("User is already muted.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    await message.delete()

    chat_id = message.chat.id
    user_id = user.id
    warning_count = get_warning_count(chat_id, user_id) + 1

    mute_duration = mute_durations.get(warning_count)
    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    if warning_count >= 5:
        await message.chat.restrict_member(user_id=user_id)
        mute_message = (
            f'<a href="tg://user?id={user_id}">{full_name}</a> has been muted forever due to multiple warnings.'
            + reason
        )
        set_warning_count(chat_id, user_id, 0)

    elif mute_duration:
        await message.chat.restrict_member(
            user_id=user_id, until_date=message.date + mute_duration
        )
        next_action = "forever" if warning_count == 4 else "for 1 day"
        mute_message = (
            f'<a href="tg://user?id={user_id}">{full_name}</a> has been muted for {get_strtime(mute_duration)}.\n'
            f"Next time will be muted {next_action}.\nWarns: {warning_count}/5" + reason
        )
        set_warning_count(chat_id, user_id, warning_count)

    else:
        mute_message = (
            f'<a href="tg://user?id={user_id}">{full_name}</a> has been warned.\n'
            f"Warns: {warning_count}/3" + reason
        )
        set_warning_count(chat_id, user_id, warning_count)

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Cancel Mute",
                    callback_data=mute_cb.new(user_id=user_id, action="cancel"),
                )
            ]
        ]
    )
    await message_sender(
        mute_message, reply_markup=keyboard if warning_count >= 3 else None
    )

    if warning_count >= 3:
        muted_count = get_muted_count(chat_id, user_id) + 1
        set_muted_count(chat_id, user_id, muted_count)


def register_warn_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(warn_user, filters.command("warn") & filters.group), 0
    )
