from aiogram import Dispatcher
from aiogram import types
from utils.chatmember import is_admin, is_banned
from utils.userid import extract_user_id


async def unban_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    user_id = await extract_user_id(message.get_args())

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif user_id:
        user = await message.bot.get_chat(user_id)
        message_sender = message.answer

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    if not await is_banned(message.chat, user):
        await message.reply("User is not banned.")
        return

    await message.delete()
    await message.chat.unban(user_id=user.id)

    await message_sender(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unbanned.'
    )


def register_unban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        unban_user,
        commands=["unban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
