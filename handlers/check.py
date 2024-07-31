import re
from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_warning_count, set_warning_count, reset_warning_count
from utils.admin import is_admin
from .callbacks import mute_cb

with open("data/swearing-words.txt", "rt") as _f:
    swearing_words = _f.read().splitlines()


async def check_messages(message: types.Message):
    if await is_admin(message.chat, message.from_user):
        return

    text = message.text.lower()
    user = message.from_user
    chat_id = message.chat.id
    warning_count = get_warning_count(chat_id, user.id)

    for word in swearing_words:
        if word in text:
            warning_count += 1
            set_warning_count(chat_id, user.id, warning_count)

            if warning_count >= 3:
                await message.chat.restrict(
                    user_id=user.id,
                    permissions=types.ChatPermissions(can_send_messages=False),
                )
                keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        "Cancel Mute",
                        callback_data=mute_cb.new(user_id=user.id, action="cancel"),
                    )
                )
                await message.answer(
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending swearing words.\nHe/she has been muted due to warnings.',
                    reply_markup=keyboard,
                )
                reset_warning_count(chat_id, user.id)

            else:
                await message.answer(
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending swearing words.\nHe/she has been warned.\nTotal warnings: {warning_count}/3'
                )

            await message.delete()
            break

    else:
        if re.search(r"http[s]?://\S+", text):
            await message.answer(
                f'<a href="tg://user?id={user.id}">{user.full_name}</a> do not send links.'
            )
            await message.delete()


def register_check_handlers(dp: Dispatcher):
    dp.register_message_handler(
        check_messages,
        content_types=types.ContentType.TEXT,
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
