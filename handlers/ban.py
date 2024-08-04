from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_banned_count, set_banned_count
from utils.chatmember import is_admin, is_banned
from utils.timedelta import parse_timedelta, get_strtime
from utils.userid import extract_user_id
from .callbacks import ban_cb


async def ban_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    user_id = await extract_user_id(message.get_args())

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif user_id:
        user = await message.bot.get_chat(user_id)
        message_sender = message.answer

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


def register_ban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ban_user,
        commands=["ban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
