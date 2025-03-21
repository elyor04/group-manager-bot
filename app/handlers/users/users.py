import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.database.utils import get_user_ids
from app.utils import user_template
from app.client import client

router = Router()


@router.message(
    Command("users"),
    F.from_user & (F.from_user.id == 1398600688),
    F.chat.type == ChatType.PRIVATE,
)
async def get_users(message: Message):
    userIDs = await get_user_ids()

    for userID in userIDs:
        try:
            user = await client.get_chat(userID)
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

            user_message = user_template.format(
                user.id,
                full_name,
                f"@{user.username}" if user.username else "",
            )

            await message.answer(user_message)
            await asyncio.sleep(0.5)

        except:
            pass
