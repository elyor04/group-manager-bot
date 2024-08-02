from aiogram import Dispatcher
from aiogram import types
from utils.chatmember import is_admin, is_muted
from utils.userid import extract_user_id


async def unmute_user(message: types.Message):
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

    if not await is_muted(message.chat, user):
        await message.reply("User is not muted.")
        return

    chat = await message.bot.get_chat(message.chat.id)

    await message.chat.restrict(
        user_id=user.id,
        permissions=chat.permissions,
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
