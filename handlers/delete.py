from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from utils.chatMember import is_admin


async def delete_message(client: Client, message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the message you want to delete.")
        return

    await message.delete()
    await message.reply_to_message.delete()


def register_delete_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(delete_message, filters.command("delete") & filters.group), 0
    )
