from aiogram import Dispatcher, types

message_template = """
📣 <b>Message has been sent to the group admins</b> 📣

👥 <b>Group</b>: <a href="https://t.me/c/{0}">{1}</a>
👱 <b>User</b>: <a href="tg://user?id={2}">{3}</a>
🔗 <b>Message link</b>: <a href="https://t.me/c/{0}/{4}">here</a>

💬 <b>Message</b> 💬

{5}
"""


async def send_to_admins(message: types.Message):
    chat = message.chat
    user = message.from_user

    message_send = message_template.format(
        str(chat.id)[4:],
        chat.title,
        user.id,
        user.full_name,
        message.message_id,
        message.text,
    )

    chat_admins = await message.chat.get_administrators()
    admin_ids = [admin.user.id for admin in chat_admins]

    for admin_id in admin_ids:
        try:
            await message.bot.send_message(admin_id, message_send)
        except:
            pass

    await message.reply("Message has been sent to the group admins.")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(
        send_to_admins,
        _admin_mention_filter,
        content_types=types.ContentType.TEXT,
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )


def _admin_mention_filter(message: types.Message):
    return message.text.lower().startswith("@admin")
