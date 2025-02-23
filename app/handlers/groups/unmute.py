from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram.filters import Command
from app.helpers import is_admin, is_muted, extract_args

router = Router()


@router.message(
    Command("unmute"),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def unmute_user(message: Message):
    if not await is_admin(message.chat, message.bot):
        await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        message_sender = message.answer

    else:
        await message.reply("Please reply to a user or specify a username.")
        return

    if not await is_muted(message.chat, user):
        await message.reply("User is not muted.")
        return

    await message.delete()
    chat = await message.bot.get_chat(message.chat.id)

    await message.chat.restrict(
        user_id=user.id,
        permissions=chat.permissions,
    )

    await message_sender(
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unmuted.',
    )
