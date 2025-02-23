from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType

router = Router()


@router.message(
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def count_messages(message: Message):
    pass
