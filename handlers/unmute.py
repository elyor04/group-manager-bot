from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from utils.chatMember import is_admin, is_muted
from utils.extractArgs import extract_args


async def unmute_user(client: Client, message: types.Message):
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

    if not await is_muted(message.chat, user):
        await message.reply("User is not muted.")
        return

    await message.delete()
    chat = await client.get_chat(message.chat.id)
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    await message.chat.restrict_member(
        user_id=user.id,
        permissions=chat.permissions,
    )

    await message_sender(
        f'<a href="tg://user?id={user.id}">{full_name}</a> has been unmuted.'
    )


def register_unmute_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(unmute_user, filters.command("unmute") & filters.group), 0
    )
