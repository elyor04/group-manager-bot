from aiogram import Dispatcher, types
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
"""


async def user_info(message: types.Message):
    args_dict = await extract_args(message.get_args())

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

    info = info_template.format(
        user.id,
        user.full_name,
        f"@{user.username}" if user.username else "",
        status.capitalize(),
        get_message_count(chat.id, user.id),
        get_warning_count(chat.id, user.id),
        get_muted_count(chat.id, user.id),
        get_banned_count(chat.id, user.id),
    )

    await message_sender(info)


def register_info_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_info,
        commands=["info"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
