from aiogram import Dispatcher
from aiogram import types

allowed_users = [7084938423, 1398600688]


async def write_by_bot(message: types.Message):
    if (message.from_user.id not in allowed_users) or (not message.get_args()):
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.answer

    await message.delete()
    await message_sender(message.get_args())

    await message.answer(str(message.chat.id))


def register_write_handlers(dp: Dispatcher):
    dp.register_message_handler(
        write_by_bot,
        commands=["write"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
