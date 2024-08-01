from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import (
    get_warning_count,
    set_warning_count,
    get_muted_count,
    set_muted_count,
)
from utils.chatmember import is_admin, is_muted, is_banned
from utils.username import extract_username
from .callbacks import mute_cb


async def warn_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    username = extract_username(message.text)

    if (not message.reply_to_message) and (not username):
        await message.reply("Please reply to the user you want to warn.")
        return

    if await is_admin(message.chat, message.reply_to_message.from_user):
        await message.reply("You cannot warn an admin.")
        return

    if await is_muted(message.chat, message.reply_to_message.from_user):
        await message.reply("User is already muted.")
        return

    if await is_banned(message.chat, message.reply_to_message.from_user):
        await message.reply("User is already banned.")
        return

    user = message.reply_to_message.from_user
    chat_id = message.chat.id
    warning_count = get_warning_count(chat_id, user.id)
    warning_count += 1
    set_warning_count(chat_id, user.id, warning_count)

    if warning_count >= 5:
        await message.chat.restrict(
            user_id=user.id, permissions=types.ChatPermissions(can_send_messages=False)
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Mute",
                callback_data=mute_cb.new(user_id=user.id, action="cancel"),
            )
        )
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted due to multiple warnings.',
            reply_markup=keyboard,
        )
        set_warning_count(chat_id, user.id, 0)

        muted_count = get_muted_count(chat_id, user.id)
        set_muted_count(chat_id, user.id, muted_count + 1)

    else:
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been warned.\nCurrent warnings: {warning_count}/5'
        )

    await message.delete()


def register_warn_handlers(dp: Dispatcher):
    dp.register_message_handler(
        warn_user,
        commands=["warn"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
