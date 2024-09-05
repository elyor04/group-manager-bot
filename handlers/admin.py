from aiogram import Dispatcher, types, enums, F

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

    admin_ids = [admin.user.id for admin in await message.chat.get_administrators()]

    for admin_id in admin_ids:
        try:
            await message.bot.send_message(admin_id, message_send)
        except:
            pass

    await message.reply("Message has been sent to the group admins.")


def register_admin_handlers(dp: Dispatcher):
    dp.message.register(
        send_to_admins,
        F.content_type == enums.ContentType.TEXT,
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
        _admin_filter,
    )


def _admin_filter(message: types.Message):
    return message.text.lower().startswith("@admin")
