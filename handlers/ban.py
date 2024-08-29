from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_banned_count, set_banned_count
from utils.chatMember import is_admin, is_banned
from utils.extractArgs import extract_args, get_strtime
from .callbacks import ban_cb


async def ban_user(client: Client, message: types.Message):
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
        await message.reply("You cannot ban an admin.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    await message.delete()

    ban_duration = args_dict["timedelta"]
    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    if ban_duration:
        until_date = message.date + ban_duration

        await message.chat.ban_member(
            user_id=user.id,
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Cancel Ban",
                        callback_data=ban_cb.new(user_id=user.id, action="cancel"),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{full_name}</a> has been banned.\nDuration: {get_strtime(ban_duration)}'
            + reason,
            reply_markup=keyboard,
        )

    else:
        await message.chat.ban_member(user_id=user.id)
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Cancel Ban",
                        callback_data=ban_cb.new(user_id=user.id, action="cancel"),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{full_name}</a> has been banned.'
            + reason,
            reply_markup=keyboard,
        )

    banned_count = get_banned_count(message.chat.id, user.id)
    set_banned_count(message.chat.id, user.id, banned_count + 1)


def register_ban_handlers(dp: Dispatcher):
    dp.add_handler(MessageHandler(ban_user, filters.command("ban") & filters.group), 0)
