from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Awaitable
from app.database.utils import get_message_count, set_message_count


class CountMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[..., Awaitable], event: TelegramObject, data: dict):
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        chat = event.chat

        message_count = await get_message_count(chat.id, user.id) + 1
        await set_message_count(chat.id, user.id, message_count)

        return await handler(event, data)
