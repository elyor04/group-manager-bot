import re
from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import get_warning_count, set_warning_count
from database.utils import get_swearing_words
from utils.chatmember import is_admin
from .callbacks import mute_cb

swearing_words = get_swearing_words()


async def check_messages(message: types.Message):
    if await is_admin(message.chat, message.from_user):
        return

    text = message.text.lower()
    user = message.from_user
    chat_id = message.chat.id
    warning_count = get_warning_count(chat_id, user.id)

    for word in swearing_words:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            warning_count += 1
            set_warning_count(chat_id, user.id, warning_count)

            if warning_count >= 5:
                await message.chat.restrict(
                    user_id=user.id,
                )
                keyboard = InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        "Cancel Mute",
                        callback_data=mute_cb.new(user_id=user.id, action="cancel"),
                    )
                )
                await message.answer(
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending swearing words.\nHe/she has been muted due to multiple warns.',
                    reply_markup=keyboard,
                )
                set_warning_count(chat_id, user.id, 0)

            else:
                await message.answer(
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending swearing words.\nHe/she has been warned.\nWarns: {warning_count}/5'
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
