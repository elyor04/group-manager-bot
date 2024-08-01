from aiogram import Dispatcher
from aiogram import types
from utils.chatmember import is_admin, is_banned
from utils.username import extract_username


async def unban_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    username = extract_username(message.text)

    if (not message.reply_to_message) and (not username):
        await message.reply("Please reply to the user you want to unban.")
        return

    if not await is_banned(message.chat, message.reply_to_message.from_user):
        await message.reply("User is not banned.")
        return

    user = message.reply_to_message.from_user
    await message.chat.unban(user_id=user.id)

    await message.answer(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unbanned.'
    )
    await message.delete()


def register_unban_handlers(dp: Dispatcher):
    dp.register_message_handler(
        unban_user,
        commands=["unban"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
