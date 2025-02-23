from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command

router = Router()


@router.message(
    Command("start"),
    F.chat.type == ChatType.PRIVATE,
)
async def start_func(message: Message):
    user = message.from_user
    await message.answer(
        f'Hello, <a href="tg://user?id={user.id}">{user.full_name}</a>\nAdd me to a group as an admin!',
    )
