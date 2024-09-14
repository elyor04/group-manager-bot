from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus
from utils.extractArgs import get_args

allowed_users = {
    # "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015, 7084938423],
}


async def write_by_bot(message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)

    args_text = get_args(message.text)
    member = await message.chat.get_member(user_id)

    allowed_ids = allowed_users["all"]
    allowed_ids.extend(allowed_users.get(chat_id, []))

    if not (
        args_text
        and ((user_id in allowed_ids) or (member.status == ChatMemberStatus.CREATOR))
    ):
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.answer

    await message.delete()
    await message_sender(args_text)


def register_write_handlers(dp: Dispatcher):
    dp.message.register(
        write_by_bot,
        Command("write"),
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
