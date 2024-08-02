from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_muted_count, set_muted_count, set_username
from utils.chatmember import is_admin, is_muted, is_banned
from utils.timedelta import parse_timedelta, get_strtime
from utils.username import extract_username
from .callbacks import mute_cb


async def mute_user(message: types.Message):
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
        await message.reply("You cannot mute an admin.")
        return

    if await is_muted(message.chat, user):
        await message.reply("User is already muted.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    mute_duration = parse_timedelta(message.get_args())

    if mute_duration:
        until_date = message.date + mute_duration

        await message.chat.restrict(
            user_id=user.id,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Mute",
                callback_data=mute_cb.new(user_id=user.id, action="cancel"),
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.\nDuration: {get_strtime(mute_duration)}',
            reply_markup=keyboard,
        )

    else:
        await message.chat.restrict(
            user_id=user.id,
            permissions=types.ChatPermissions(can_send_messages=False),
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Mute",
                callback_data=mute_cb.new(user_id=user.id, action="cancel"),
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.',
            reply_markup=keyboard,
        )

    muted_count = get_muted_count(message.chat.id, user.id)
    set_muted_count(message.chat.id, user.id, muted_count + 1)

    await message.delete()


def register_mute_handlers(dp: Dispatcher):
    dp.register_message_handler(
        mute_user,
        commands=["mute"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
