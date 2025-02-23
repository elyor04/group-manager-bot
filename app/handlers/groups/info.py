from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.database.utils import get_warning_count, get_muted_count, get_banned_count, get_message_count
from app.helpers import user_status, is_admin, extract_args
from app.utils import info_template
from app.client import client

router = Router()


@router.message(
    Command("info"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def user_info(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        message_sender = message.answer

    else:
        user = message.from_user
        message_sender = message.answer

    await message.delete()

    chat = message.chat
    status = await user_status(chat, user)
    member = await client.get_chat_member(chat.id, user.id)
    joined_date = member.joined_date.strftime("%d/%m/%Y") if member.joined_date else ""

    info = info_template.format(
        user.id,
        user.full_name,
        f"@{user.username}" if user.username else "",
        status.capitalize(),
        await get_message_count(chat.id, user.id),
        await get_warning_count(chat.id, user.id),
        await get_muted_count(chat.id, user.id),
        await get_banned_count(chat.id, user.id),
        joined_date,
    )

    await message_sender(info)
