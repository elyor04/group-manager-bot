from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler


async def start_func(client: Client, message: types.Message):
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    await client.send_message(
        message.chat.id,
        f'Hello, <a href="tg://user?id={user.id}">{full_name}</a>\nAdd me to a group as an admin!',
    )


def register_start_handlers(app: Client):
    app.add_handler(
        MessageHandler(start_func, filters.command("start") & filters.private)
    )
