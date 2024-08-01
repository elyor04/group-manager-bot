from aiogram import Dispatcher
from aiogram import types
from aiogram.types import ChatPermissions
from utils.chatmember import is_admin, is_muted


async def unmute_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    if not message.reply_to_message:
        await message.reply("Please reply to the user you want to mute.")
        return

    if not await is_muted(message.chat, message.reply_to_message.from_user):
        await message.reply("User is not muted.")
        return

    user = message.reply_to_message.from_user
    await message.chat.restrict(
        user_id=user.id,
        permissions=ChatPermissions(can_send_messages=True),
    )

    await message.answer(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unmuted.'
    )
    await message.delete()


def register_unmute_handlers(dp: Dispatcher):
    dp.register_message_handler(
        unmute_user,
        commands=["unmute"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
