from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import timedelta
from database.models import get_warning_count, set_warning_count, reset_warning_count
from utils.admin import is_admin
from .callbacks import mute_cb


async def warn_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the user you want to warn.")
        return

    if await is_admin(message.chat, message.reply_to_message.from_user):
        await message.reply("You cannot warn an admin.")
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
        await message.reply(
            f"User <b>{user.full_name}</b> has been muted forever due to multiple warnings.",
            reply_markup=keyboard,
        )
        reset_warning_count(chat_id, user.id)

    elif warning_count >= 3:
        until_date = message.date + timedelta(hours=1)
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
        await message.reply(
            f"User <b>{user.full_name}</b> has been muted for 1 hour. Total warnings: {warning_count}/5",
            reply_markup=keyboard,
        )

    else:
        await message.reply(
            f"User <b>{user.full_name}</b> has been warned. Total warnings: {warning_count}/3"
        )


def register_warn_handlers(dp: Dispatcher):
    dp.register_message_handler(
        warn_user,
        commands=["warn"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
