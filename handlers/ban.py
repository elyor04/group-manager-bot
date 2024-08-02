from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_banned_count, set_banned_count, set_username
from utils.chatmember import is_admin, is_banned
from utils.timedelta import parse_timedelta, get_strtime
from utils.username import extract_username
from .callbacks import ban_cb


async def ban_user(message: types.Message):
    set_username(message.chat.id, message.from_user.id, message.from_user.username)

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    username = extract_username(message.get_args())

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif username:
        user = await message.bot.get_chat(username)
        message_sender = message.answer

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    set_username(message.chat.id, user.id, user.username)

    if await is_admin(message.chat, user):
        await message.reply("You cannot ban an admin.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    ban_duration = parse_timedelta(message.get_args())

    if ban_duration:
        until_date = message.date + ban_duration

        await message.chat.kick(
            user_id=user.id,
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Ban", callback_data=ban_cb.new(user_id=user.id, action="cancel")
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned.\nDuration: {get_strtime(ban_duration)}',
            reply_markup=keyboard,
        )

    else:
        await message.chat.kick(user_id=user.id)
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Ban", callback_data=ban_cb.new(user_id=user.id, action="cancel")
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned.',
            reply_markup=keyboard,
        )

    banned_count = get_banned_count(message.chat.id, user.id)
    set_banned_count(message.chat.id, user.id, banned_count + 1)

    await message.delete()


def register_ban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ban_user,
        commands=["ban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
