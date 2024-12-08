from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from ..utils.chatMember import is_admin
from ..utils.silenceMember import unsilence_member, is_silenced
from ..utils.extractArgs import extract_args


async def unsilence_user(message: types.Message):
    if not await is_admin(message.chat, message.bot):
        # await message.reply("Please make me an admin first.")
        return

    if not await is_admin(message.chat, message.from_user):
        # await message.reply("You are not an admin of this group.")
        return

    args_dict = await extract_args(message.text)

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        # message_sender = message.reply_to_message.reply

    elif args_dict["user"]:
        user = args_dict["user"]
        # message_sender = message.answer

    else:
        # await message.reply("Please reply to a user or specify a username.")
        return

    if not await is_silenced(message.chat.id, user.id):
        # await message.reply("User is not silenced.")
        return

    await message.delete()
    unsilence_member(message.chat.id, user.id)


def register_unsilence_handlers(dp: Dispatcher):
    dp.message.register(
        unsilence_user,
        Command("unsilence"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
