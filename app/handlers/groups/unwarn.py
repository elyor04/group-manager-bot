from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.database.utils import get_warning_count, set_warning_count
from app.helpers import is_admin, extract_args

router = Router()


@router.message(
    Command("unwarn"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def unwarn_user(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        message_sender = message.answer

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    chat_id = message.chat.id
    warning_count = await get_warning_count(chat_id, user.id)
    warning_count -= 1

    if warning_count >= 0:
        await message.delete()

        await message_sender(f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unwarned.\nWarns: {warning_count}/5')
        await set_warning_count(chat_id, user.id, warning_count)

    else:
        await message.reply("User has no warns.")
