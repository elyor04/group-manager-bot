from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import (
    get_warning_count,
    set_warning_count,
    get_muted_count,
    set_muted_count,
)
from utils.chatMember import is_admin, is_muted, is_banned
from utils.extractArgs import extract_args
from .callbacks import mute_cb


async def warn_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.get_args())

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user_id"]:
        user = await message.bot.get_chat(args_dict["user_id"])
        message_sender = message.answer

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
    warning_count = get_warning_count(chat_id, user.id)
    warning_count += 1

    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""

    if warning_count >= 5:
        await message.chat.restrict(
            user_id=user.id,
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Mute",
                callback_data=mute_cb.new(user_id=user.id, action="cancel"),
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted due to multiple warns.',
            reply_markup=keyboard,
        )
        set_warning_count(chat_id, user.id, 0)

        muted_count = get_muted_count(chat_id, user.id)
        set_muted_count(chat_id, user.id, muted_count + 1)

    else:
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been warned.\nWarns: {warning_count}/5'
            + reason
        )
        set_warning_count(chat_id, user.id, warning_count)


def register_warn_handlers(dp: Dispatcher):
    dp.register_message_handler(
        warn_user,
        commands=["warn"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
