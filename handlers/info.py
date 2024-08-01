from aiogram import Dispatcher
from aiogram import types
from utils.chatmember import user_status
from database.models import get_warning_count, get_muted_count, get_banned_count


async def user_info(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Please reply to the user you want to mute.")
        return

    chat = message.chat
    user = message.reply_to_message.from_user
    status = await user_status(chat, user)

    info = f'Info about: <a href="tg://user?id={user.id}">{user.full_name}</a>\nCurrent status: {status.capitalize()}\nCurrent warnings: {get_warning_count(chat.id, user.id)}/5\nTotal muted: {get_muted_count(chat.id, user.id)}\nTotal banned: {get_banned_count(chat.id, user.id)}'

    await message.answer(info)
    await message.delete()


def register_info_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_info,
        commands=["info"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
