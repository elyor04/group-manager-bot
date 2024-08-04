from aiogram import Dispatcher
from aiogram import types

allowed_users = {
    "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015],
}


async def write_by_bot(message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)

    if user_id in allowed_users["all"]:
        pass
    elif user_id in allowed_users.get(chat_id, []):
        pass
    else:
        return

    if not message.get_args():
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.answer

    await message.delete()
    await message_sender(message.get_args())

    await message.answer()


def register_write_handlers(dp: Dispatcher):
    dp.register_message_handler(
        write_by_bot,
        commands=["write"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
