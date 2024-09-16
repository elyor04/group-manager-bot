from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from utils.chatMember import is_admin


async def delete_message(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        return

    if not message.reply_to_message:
        return

    await message.delete()
    await message.reply_to_message.delete()


def register_delete_handlers(dp: Dispatcher):
    dp.message.register(
        delete_message,
        Command("delete"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
