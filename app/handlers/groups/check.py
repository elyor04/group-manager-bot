import re
from datetime import timedelta
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType as AiogramChatType
from pyrogram.enums import ChatType as PyrogramChatType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from app.database.utils import get_warning_count, set_warning_count, get_muted_count, set_muted_count
from app.helpers import get_bad_words, is_admin, get_strtime, extract_args
from app.utils import MuteCallbackData

router = Router()

swearing_words = get_bad_words()
mute_durations = {
    3: timedelta(hours=1),
    4: timedelta(days=1),
}


@router.message(
    F.text,
    F.chat.type.in_([AiogramChatType.GROUP, AiogramChatType.SUPERGROUP]),
)
async def check_messages(message: Message):
    if not await is_admin(message.chat, message.bot):
        return

    if await is_admin(message.chat, message.from_user):
        return

    user = message.from_user
    chat = message.chat
    text = message.text.lower()
    warning_count = await get_warning_count(chat.id, user.id)

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
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending bad words.\nHe/she has been muted forever due to multiple warnings.'
                )
                await set_warning_count(chat.id, user.id, 0)

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
                await set_warning_count(chat.id, user.id, warning_count)

            else:
                mute_message = (
                    f'<a href="tg://user?id={user.id}">{user.full_name}</a> is sending bad words.\nHe/she has been warned.\n' f"Warns: {warning_count}/3"
                )
                await set_warning_count(chat.id, user.id, warning_count)

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Cancel Mute",
                            callback_data=MuteCallbackData(user_id=user.id, action="cancel").pack(),
                        )
                    ]
                ]
            )
            await message.answer(mute_message, reply_markup=keyboard if warning_count >= 3 else None)

            if warning_count >= 3:
                muted_count = await get_muted_count(chat.id, user.id) + 1
                await set_muted_count(chat.id, user.id, muted_count)

            return

    if re.search(
        r"\b(?:https?:\/\/)?(?:www\.)?([a-z0-9-]+\.(com|net|org|gov|edu|info|io|co|biz|me|us|uk|ca|de|ru|uz|fr|au|in|jp|cn|nl|br|it|es|pl|kr|mx|se|ch|be|nz))([^\s]*)\b",
        text,
    ):
        await message.delete()
        await message.answer(f'<a href="tg://user?id={user.id}">{user.full_name}</a> do not send links.')
        return

    args_dict = await extract_args(message.text, False)

    if args_dict["user"] and (args_dict["user"].type != PyrogramChatType.PRIVATE):
        await message.delete()
        await message.answer(f'<a href="tg://user?id={user.id}">{user.full_name}</a> do not share chats.')
        return
