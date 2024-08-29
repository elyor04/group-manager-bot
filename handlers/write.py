from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from utils.extractArgs import get_args

allowed_users = {
    # "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015, 7084938423],
}


async def write_by_bot(client: Client, message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)
    args_text = get_args(message.text)

    if (
        (user_id not in allowed_users["all"])
        and (user_id not in allowed_users.get(chat_id, []))
    ) or (not args_text):
        return

    if message.reply_to_message:
        message_sender = message.reply_to_message.reply
    else:
        message_sender = message.reply

    await message.delete()
    await message_sender(args_text)


def register_write_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(write_by_bot, filters.command("write") & filters.group), 0
    )
