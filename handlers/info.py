from aiogram import Dispatcher
from aiogram import types
from database.models import get_warning_count, get_muted_count, get_banned_count
from utils.chatmember import user_status
from utils.username import extract_username


async def user_info(message: types.Message):
    username = extract_username(message.get_args())

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif username:
        user = await message.bot.get_chat(username)
        message_sender = message.answer

    else:
        user = message.from_user
        message_sender = message.answer

    chat = message.chat
    status = await user_status(chat, user)

    info = f'Info about: <a href="tg://user?id={user.id}">{user.full_name}</a>\nCurrent status: {status.capitalize()}\nCurrent warnings: {get_warning_count(chat.id, user.id)}/5\nTotal muted: {get_muted_count(chat.id, user.id)}\nTotal banned: {get_banned_count(chat.id, user.id)}'

    await message_sender(info)
    await message.delete()


def register_info_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_info,
        commands=["info"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
