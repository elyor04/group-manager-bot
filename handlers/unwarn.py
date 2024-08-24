from aiogram import Dispatcher, types
from database.models import get_warning_count, set_warning_count
from utils.chatMember import is_admin
from utils.extractArgs import extract_args


async def unwarn_user(message: types.Message):
    if not await is_admin(message.chat, message.from_user):
        await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.get_args())

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
    dp.register_message_handler(
        unwarn_user,
        commands=["unwarn"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
