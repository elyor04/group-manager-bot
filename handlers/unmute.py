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
        message_id = message.reply_to_message.id

    elif args_dict["username"]:
        user = await client.get_chat(args_dict["username"])
        message_id = None

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    if not await is_muted(message.chat, user):
        await message.reply("User is not muted.")
        return

    await message.delete()
    permissions = message.chat.permissions
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    await message.chat.restrict_member(
        user_id=user.id,
        permissions=permissions,
    )

    await client.send_message(
        message.chat.id,
        f'<a href="tg://user?id={user.id}">{full_name}</a> has been unmuted.',
        reply_to_message_id=message_id,
    )


def register_unmute_handlers(app: Client):
    app.add_handler(
        MessageHandler(unmute_user, filters.command("unmute") & filters.group)
    )
