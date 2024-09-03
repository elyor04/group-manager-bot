from aiogram import Dispatcher, types
from database.models import get_message_count, set_message_count


async def count_messages(message: types.Message):
    user = message.from_user
    chat = message.chat

    message_count = get_message_count(chat.id, user.id) + 1
    set_message_count(chat.id, user.id, message_count)


def register_count_handlers(dp: Dispatcher):
    dp.register_message_handler(
        count_messages,
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
