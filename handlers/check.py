import re
from aiogram import Dispatcher, types, enums, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
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
from utils.callbackData import MuteCallbackData

swearing_words = get_swearing_words()
mute_durations = {
    3: timedelta(hours=1),
    4: timedelta(days=1),
}


async def check_messages(message: types.Message):
    user = message.from_user
    chat = message.chat

    message_count = get_message_count(chat.id, user.id) + 1
    set_message_count(chat.id, user.id, message_count)

    if await is_admin(chat, user):
        return

    text = message.text.lower()
    warning_count = get_warning_count(chat.id, user.id)

    for word in swearing_words:
        if re.search(r"\b" + re.escape(word) + r"\b", text):
            await message.delete()

            warning_count += 1
            mute_duration = mute_durations.get(warning_count)

            if warning_count >= 5:
                await message.chat.restrict(
                    user_id=user.id,
                    permissions=ChatPermissions(),
                )
                mute_message = f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending bad words.\nHe/she has been muted forever due to multiple warnings.'
                set_warning_count(chat.id, user.id, 0)

            elif mute_duration:
                await message.chat.restrict(
                    user_id=user.id,
                    permissions=ChatPermissions(),
                    until_date=message.date + mute_duration,
                )
                next_action = "forever" if warning_count == 4 else "for 1 day"
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending bad words.\nHe/she has been muted for {get_strtime(mute_duration)}.\n'
                    f"Next time will be muted {next_action}.\nWarns: {warning_count}/5"
                )
                set_warning_count(chat.id, user.id, warning_count)

            else:
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending bad words.\nHe/she has been warned.\n'
                    f"Warns: {warning_count}/3"
                )
                set_warning_count(chat.id, user.id, warning_count)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Cancel Mute",
                            callback_data=MuteCallbackData(
                                user_id=user.id, action="cancel"
                            ).pack(),
                        )
                    ]
                ]
            )
            await message.answer(
                mute_message, reply_markup=keyboard if warning_count >= 3 else None
            )

            if warning_count >= 3:
                muted_count = get_muted_count(chat.id, user.id) + 1
                set_muted_count(chat.id, user.id, muted_count)

            return

    if re.search(r"http[s]?://\S+", text):
        await message.delete()
        await message.answer(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> do not send links.'
        )
        return


def register_check_handlers(dp: Dispatcher):
    dp.message.register(
        check_messages,
        F.content_type == enums.ContentType.TEXT,
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
