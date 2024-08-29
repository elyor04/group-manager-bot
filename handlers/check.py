import re
from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import (
    get_warning_count,
    set_warning_count,
    get_muted_count,
    set_muted_count,
    get_message_count,
    set_message_count,
)
from database.utils import get_swearing_words
from utils.chatMember import is_admin
from utils.extractArgs import get_strtime
from datetime import timedelta
from .callbacks import mute_cb

swearing_words = get_swearing_words()
mute_durations = {
    3: timedelta(hours=1),
    4: timedelta(days=1),
}


async def check_messages(client: Client, message: types.Message):
    user = message.from_user
    chat = message.chat

    message_count = get_message_count(chat.id, user.id) + 1
    set_message_count(chat.id, user.id, message_count)

    if await is_admin(chat, user):
        return

    text = message.text.lower()
    warning_count = get_warning_count(chat.id, user.id)
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    for word in swearing_words:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            await message.delete()

            warning_count += 1
            mute_duration = mute_durations.get(warning_count)

            if warning_count >= 5:
                await message.chat.restrict_member(user_id=user.id)
                mute_message = f'<a href="tg://user?id={user.id}">{full_name}</a> is sending bad words.\nHe/she has been muted forever due to multiple warnings.'
                set_warning_count(chat.id, user.id, 0)

            elif mute_duration:
                await message.chat.restrict_member(
                    user_id=user.id, until_date=message.date + mute_duration
                )
                next_action = "forever" if warning_count == 4 else "for 1 day"
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{full_name}</a> is sending bad words.\nHe/she has been muted for {get_strtime(mute_duration)}.\n'
                    f"Next time will be muted {next_action}.\nWarns: {warning_count}/5"
                )
                set_warning_count(chat.id, user.id, warning_count)

            else:
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{full_name}</a> is sending bad words.\nHe/she has been warned.\n'
                    f"Warns: {warning_count}/3"
                )
                set_warning_count(chat.id, user.id, warning_count)

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Cancel Mute",
                            callback_data=mute_cb.new(user_id=user.id, action="cancel"),
                        )
                    ]
                ]
            )
            await message.reply(
                mute_message, reply_markup=keyboard if warning_count >= 3 else None
            )

            if warning_count >= 3:
                muted_count = get_muted_count(chat.id, user.id) + 1
                set_muted_count(chat.id, user.id, muted_count)

            return

    if re.search(r"http[s]?://\S+", text):
        await message.delete()
        await message.reply(
            f'<a href="tg://user?id={user.id}">{full_name}</a> do not send links.'
        )
        return


def register_check_handlers(dp: Dispatcher):
    dp.add_handler(MessageHandler(check_messages, filters.text & filters.group), 0)
