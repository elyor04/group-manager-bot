from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.admin import is_admin
from utils.timedelta import parse_timedelta
from .callbacks import mute_cb


async def mute_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the user you want to mute.")
        return

    if await is_admin(message.chat, message.reply_to_message.from_user):
        await message.reply("You cannot mute an admin.")
        return

    user = message.reply_to_message.from_user
    mute_duration = parse_timedelta(message.text)

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
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted for {mute_duration}',
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
        await message.reply_to_message.reply(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.',
            reply_markup=keyboard,
        )

    await message.delete()


def register_mute_handlers(dp: Dispatcher):
    dp.register_message_handler(
        mute_user,
        commands=["mute"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
