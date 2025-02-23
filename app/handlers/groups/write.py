from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.helpers import get_args, is_admin

router = Router()


@router.message(
    Command("write"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def write_by_bot(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.answer

    args_text = get_args(message.text)

    await message.delete()
    if args_text:
        await message_sender(args_text)
