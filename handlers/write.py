from aiogram import Dispatcher
from aiogram import types

allowed_users = {
    "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015],
}


async def write_by_bot(message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)

    if (
        (user_id not in allowed_users["all"])
        and (user_id not in allowed_users.get(chat_id, []))
    ) or (not message.get_args()):
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.answer

    await message.delete()
    await message_sender(message.get_args())


def register_write_handlers(dp: Dispatcher):
    dp.register_message_handler(
        write_by_bot,
        commands=["write"],
        chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP],
    )
