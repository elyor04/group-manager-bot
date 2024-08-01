from aiogram import Dispatcher
from aiogram import types
from database.models import get_warning_count, get_muted_count, get_banned_count
from utils.chatmember import user_status
from utils.username import extract_username

info_template = """
🆔 <b>ID</b>: {0}
👱 <b>Name</b>: <a href="tg://user?id={0}">{1}</a>
🌐 <b>Username</b>: @{2}
👀 <b>Situation</b>: {3}
❕ <b>Warns</b>: {4}/5
🔇 <b>Muted</b>: {5}
🚫 <b>Banned</b>: {6}
"""


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

    info = info_template.format(
        user.id,
        user.full_name,
        user.username,
        status.capitalize(),
        get_warning_count(chat.id, user.id),
        get_muted_count(chat.id, user.id),
        get_banned_count(chat.id, user.id),
    )

    await message_sender(info)
    await message.delete()


def register_info_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_info,
        commands=["info"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
