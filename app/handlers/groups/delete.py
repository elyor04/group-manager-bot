from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.helpers import is_admin

router = Router()


@router.message(
    Command("delete"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def delete_message(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    await message.delete()
    if message.reply_to_message:
        await message.reply_to_message.delete()
