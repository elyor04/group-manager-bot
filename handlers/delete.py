from aiogram import Dispatcher, types
from utils.chatmember import is_admin


async def delete_message(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the message you want to delete.")
        return

    await message.delete()
    await message.reply_to_message.delete()


def register_delete_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_message,
        commands=["delete"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
