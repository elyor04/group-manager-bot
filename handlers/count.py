from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from database.models import get_message_count, set_message_count


async def count_messages(client: Client, message: types.Message):
    user = message.from_user
    chat = message.chat

    message_count = get_message_count(chat.id, user.id) + 1
    set_message_count(chat.id, user.id, message_count)


def register_count_handlers(app: Client):
    app.add_handler(MessageHandler(count_messages, filters.group))
