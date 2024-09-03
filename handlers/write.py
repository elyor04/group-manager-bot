from aiogram import Dispatcher, types
from aiogram.types import ChatMemberStatus

allowed_users = {
    # "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015, 7084938423],
}


async def write_by_bot(message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)

    allowed_ids = [
        admin.user.id
        for admin in await message.chat.get_administrators()
        if admin.status == ChatMemberStatus.OWNER
    ]

    allowed_ids.extend(allowed_users["all"])
    allowed_ids.extend(allowed_users.get(chat_id, []))

    if (user_id not in set(allowed_ids)) or (not message.get_args()):
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
