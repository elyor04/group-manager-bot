from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from database.models import get_warning_count, set_warning_count
from utils.chatMember import is_admin
from utils.extractArgs import extract_args


async def unwarn_user(client: Client, message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["username"]:
        user = await client.get_chat(args_dict["username"])
        message_sender = message.reply

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    chat_id = message.chat.id
    warning_count = get_warning_count(chat_id, user.id)
    warning_count -= 1
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    if warning_count >= 0:
        await message.delete()

        await message_sender(
            f'<a href="tg://user?id={user.id}">{full_name}</a> has been unwarned.\nWarns: {warning_count}/5'
        )
        set_warning_count(chat_id, user.id, warning_count)

    else:
        await message.reply("User has no warns.")


def register_unwarn_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(unwarn_user, filters.command("unwarn") & filters.group), 0
    )
