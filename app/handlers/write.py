from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from ..utils.extractArgs import get_args
from ..utils.chatMember import is_admin


async def write_by_bot(message: types.Message):
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


def register_write_handlers(dp: Dispatcher):
    dp.message.register(
        write_by_bot,
        Command("write"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
