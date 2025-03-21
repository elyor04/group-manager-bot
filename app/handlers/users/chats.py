import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.database.utils import get_chat_ids
from app.utils import chat_template
from app.client import client

router = Router()


@router.message(
    Command("chats"),
    F.from_user & (F.from_user.id == 1398600688),
    F.chat.type == ChatType.PRIVATE,
)
async def get_chats(message: Message):
    chatIDs = await get_chat_ids()

    for chatID in chatIDs:
        try:
            chat = await client.get_chat(chatID)

            chat_message = chat_template.format(
                chat.id,
                str(chat.id)[4:],
                chat.title,
                f"@{chat.username}" if chat.username else "",
            )

            await message.answer(chat_message)
            await asyncio.sleep(0.5)

        except:
            pass
