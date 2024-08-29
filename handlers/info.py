from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from database.models import (
    get_warning_count,
    get_muted_count,
    get_banned_count,
    get_message_count,
)
from utils.chatMember import user_status
from utils.extractArgs import extract_args

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


async def user_info(client: Client, message: types.Message):
    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["username"]:
        user = await client.get_chat(args_dict["username"])
        message_sender = message.reply

    else:
        user = message.from_user
        message_sender = message.reply

    await message.delete()

    chat = message.chat
    status = await user_status(chat, user)
    member = await chat.get_member(user.id)

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    joined_date = member.joined_date.strftime("%d/%m/%Y") if member.joined_date else ""

    info = info_template.format(
        user.id,
        full_name,
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
    dp.add_handler(
        MessageHandler(user_info, filters.command("info") & filters.group), 0
    )
