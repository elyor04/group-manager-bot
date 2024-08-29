from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_muted_count, set_muted_count
from utils.chatMember import is_admin, is_muted, is_banned
from utils.extractArgs import extract_args, get_strtime
from .callbacks import mute_cb


async def mute_user(client: Client, message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_id = message.reply_to_message.id

    elif args_dict["username"]:
        user = await client.get_chat(args_dict["username"])
        message_id = None

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
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    if mute_duration:
        until_date = message.date + mute_duration

        await message.chat.restrict_member(
            user_id=user.id,
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Cancel Mute",
                        callback_data=mute_cb.new(user_id=user.id, action="cancel"),
                    )
                ]
            ]
        )
        await client.send_message(
            message.chat.id,
            f'<a href="tg://user?id={user.id}">{full_name}</a> has been muted.\nDuration: {get_strtime(mute_duration)}'
            + reason,
            reply_markup=keyboard,
            reply_to_message_id=message_id,
        )

    else:
        await message.chat.restrict_member(
            user_id=user.id,
            permissions=types.ChatPermissions(can_send_messages=False),
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Cancel Mute",
                        callback_data=mute_cb.new(user_id=user.id, action="cancel"),
                    )
                ]
            ]
        )
        await client.send_message(
            message.chat.id,
            f'<a href="tg://user?id={user.id}">{full_name}</a> has been muted.'
            + reason,
            reply_markup=keyboard,
            reply_to_message_id=message_id,
        )

    muted_count = get_muted_count(message.chat.id, user.id)
    set_muted_count(message.chat.id, user.id, muted_count + 1)


def register_mute_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(mute_user, filters.command("mute") & filters.group), 0
    )
