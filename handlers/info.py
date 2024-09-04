from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from database.models import (
    get_warning_count,
    get_muted_count,
    get_banned_count,
    get_message_count,
)
from utils.chatMember import user_status
from utils.extractArgs import extract_args
from userbot import app

info_template = """
🆔 <b>ID</b>: {0}
👱 <b>Name</b>: <a href="tg://user?id={0}">{1}</a>
🌐 <b>Username</b>: {2}
👀 <b>Status</b>: {3}
💬 <b>Messages</b>: {4}
❕ <b>Warns</b>: {5}/5
🔇 <b>Muted</b>: {6}
🚷 <b>Banned</b>: {7}
📅 <b>Joined</b>: {8}
"""


async def user_info(message: types.Message):
    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        message_sender = message.answer

    else:
        user = message.from_user
        message_sender = message.answer

    await message.delete()

    chat = message.chat
    status = await user_status(chat, user)
    member = await app.get_chat_member(chat.id, user.id)
    joined_date = member.joined_date.strftime("%d/%m/%Y") if member.joined_date else ""

    info = info_template.format(
        user.id,
        user.full_name,
        f"@{user.username}" if user.username else "",
        status.capitalize(),
        get_message_count(chat.id, user.id),
        get_warning_count(chat.id, user.id),
        get_muted_count(chat.id, user.id),
        get_banned_count(chat.id, user.id),
        joined_date,
    )

    await message_sender(info)


def register_info_handlers(dp: Dispatcher):
    dp.message.register(
        user_info,
        Command("info"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
