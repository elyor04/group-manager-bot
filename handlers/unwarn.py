from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from database.models import get_warning_count, set_warning_count
from utils.chatMember import is_admin
from utils.extractArgs import extract_args


async def unwarn_user(message: types.Message):
    if not await is_admin(message.chat, await message.bot.get_me()):
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

    chat_id = message.chat.id
    warning_count = get_warning_count(chat_id, user.id)
    warning_count -= 1

    if warning_count >= 0:
        await message.delete()

        await message_sender(
            f'<a href="tg://user?id={user.id}">{user.full_name}</a> has been unwarned.\nWarns: {warning_count}/5'
        )
        set_warning_count(chat_id, user.id, warning_count)

    else:
        await message.reply("User has no warns.")


def register_unwarn_handlers(dp: Dispatcher):
    dp.message.register(
        unwarn_user,
        Command("unwarn"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
