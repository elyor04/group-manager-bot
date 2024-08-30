from pyrogram import Client, filters, types
from pyrogram.enums import ChatMembersFilter
from pyrogram.handlers.message_handler import MessageHandler

message_template = """
📣 <b>Message has been sent to the group admins</b> 📣

👥 <b>Group</b>: <a href="https://t.me/c/{0}">{1}</a>
👱 <b>User</b>: <a href="tg://user?id={2}">{3}</a>
🔗 <b>Message link</b>: <a href="https://t.me/c/{0}/{4}">here</a>

💬 <b>Message</b> 💬

{5}
"""


async def send_to_admins(client: Client, message: types.Message):
    chat = message.chat
    user = message.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    message_send = message_template.format(
        str(chat.id)[4:],
        chat.title,
        user.id,
        full_name,
        message.id,
        message.text,
    )

    admin_ids = [
        admin.user.id
        async for admin in message.chat.get_members(
            filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    for admin_id in admin_ids:
        try:
            await client.send_message(admin_id, message_send)
        except:
            pass

    await message.reply("Message has been sent to the group admins.")


def register_admin_handlers(app: Client):
    app.add_handler(
        MessageHandler(
            send_to_admins, filters.text & filters.group & filters.create(_admin_filter)
        )
    )


def _admin_filter(_, __, message: types.Message):
    return message.text.lower().startswith("@admin")
