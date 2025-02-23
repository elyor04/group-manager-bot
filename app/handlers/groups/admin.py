from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from app.helpers import is_admin
from app.utils import admin_template

router = Router()


@router.message(
    F.text and F.text.lower().startswith("@admin"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def send_to_admins(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    chat = message.chat
    user = message.from_user

    message_send = admin_template.format(
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
