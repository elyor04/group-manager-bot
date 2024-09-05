from aiogram import Dispatcher, BaseMiddleware
from aiogram.types import Message
from database.models import get_message_count, set_message_count


class CountMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user = event.from_user
        chat = event.chat

        message_count = get_message_count(chat.id, user.id) + 1
        set_message_count(chat.id, user.id, message_count)

        return await handler(event, data)


def register_count_middlewares(dp: Dispatcher):
    dp.message.middleware(CountMiddleware())
