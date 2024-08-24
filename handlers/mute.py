from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_muted_count, set_muted_count
from utils.chatMember import is_admin, is_muted, is_banned
from utils.extractArgs import extract_args, get_strtime
from .callbacks import mute_cb


async def mute_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.get_args())

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
        await message.reply("You cannot mute an admin.")
        return

    if await is_muted(message.chat, user):
        await message.reply("User is already muted.")
        return

    if await is_banned(message.chat, user):
        await message.reply("User is already banned.")
        return

    await message.delete()

    mute_duration = args_dict["timedelta"]
    reason = "\nReason: " + args_dict["reason"] if args_dict["reason"] else ""

    if mute_duration:
        until_date = message.date + mute_duration

        await message.chat.restrict(
            user_id=user.id,
            until_date=until_date,
        )
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Cancel Mute",
                callback_data=mute_cb.new(user_id=user.id, action="cancel"),
            )
        )
        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.\nDuration: {get_strtime(mute_duration)}'
            + reason,
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
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been muted.'
            + reason,
            reply_markup=keyboard,
        )

    muted_count = get_muted_count(message.chat.id, user.id)
    set_muted_count(message.chat.id, user.id, muted_count + 1)


def register_mute_handlers(dp: Dispatcher):
    dp.register_message_handler(
        mute_user,
        commands=["mute"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
