from aiogram import Dispatcher
from aiogram import types
from database.models import set_username
from utils.chatmember import is_admin, is_muted
from utils.username import extract_username


async def unmute_user(message: types.Message):
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

    if not await is_muted(message.chat, user):
        await message.reply("User is not muted.")
        return

    await message.chat.restrict(
        user_id=user.id,
        permissions=message.chat.permissions,
    )

    await message_sender(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unmuted.'
    )
    await message.delete()


def register_unmute_handlers(dp: Dispatcher):
    dp.register_message_handler(
        unmute_user,
        commands=["unmute"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
