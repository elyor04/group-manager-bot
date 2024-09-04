from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_banned_count, set_banned_count
from utils.chatMember import is_admin, is_banned
from utils.extractArgs import extract_args, get_strtime
from utils.callbackData import BanCallbackData


async def ban_user(message: types.Message):
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
        await message.reply("You cannot ban an admin.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    await message.delete()

    ban_duration = args_dict["timedelta"]
    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""

    if ban_duration:
        until_date = message.date + ban_duration

        await message.chat.ban(
            user_id=user.id,
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Cancel Ban",
                        callback_data=BanCallbackData(
                            user_id=user.id, action="cancel"
                        ).pack(),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned.\nDuration: {get_strtime(ban_duration)}'
            + reason,
            reply_markup=keyboard,
        )

    else:
        await message.chat.ban(user_id=user.id)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Cancel Ban",
                        callback_data=BanCallbackData(
                            user_id=user.id, action="cancel"
                        ).pack(),
                    )
                ]
            ]
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned.'
            + reason,
            reply_markup=keyboard,
        )

    banned_count = get_banned_count(message.chat.id, user.id)
    set_banned_count(message.chat.id, user.id, banned_count + 1)


def register_ban_handlers(dp: Dispatcher):
    dp.message.register(
        ban_user,
        Command("ban"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
