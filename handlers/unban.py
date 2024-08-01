from aiogram import Dispatcher
from aiogram import types
from utils.chatmember import is_admin, is_banned
from utils.username import extract_username


async def unban_user(message: types.Message):
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

    if not await is_banned(message.chat, user):
        await message.reply("User is not banned.")
        return

    await message.chat.unban(user_id=user.id)

    await message_sender(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unbanned.'
    )
    await message.delete()


def register_unban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        unban_user,
        commands=["unban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
