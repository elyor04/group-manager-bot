from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.admin import is_admin
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
    await message.chat.kick(user_id=user.id)
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "Cancel Ban", callback_data=ban_cb.new(user_id=user.id, action="cancel")
        )
    )
    await message.reply(
        f"User <b>{user.full_name}</b> has been banned for 1 day.",
        reply_markup=keyboard,
    )


def register_ban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ban_user,
        commands=["ban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
