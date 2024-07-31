from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.admin import is_admin
from utils.timedelta import parse_timedelta
from .callbacks import ban_cb


async def ban_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the user you want to ban.")
        return

    if await is_admin(message.chat, message.reply_to_message.from_user):
        await message.reply("You cannot ban an admin.")
        return

    user = message.reply_to_message.from_user
    ban_duration = parse_timedelta(message.text)

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
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned for {ban_duration}',
            reply_markup=keyboard,
        )

    else:
        await message.chat.kick(user_id=user.id)
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Ban", callback_data=ban_cb.new(user_id=user.id, action="cancel")
            )
        )
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been banned.',
            reply_markup=keyboard,
        )

    await message.delete()


def register_ban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ban_user,
        commands=["ban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
