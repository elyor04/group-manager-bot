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

    await message.delete()
    message_id = message.reply_to_message.id if message.reply_to_message else None

    await client.send_message(
        message.chat.id,
        args_text,
        reply_to_message_id=message_id,
    )


def register_write_handlers(app: Client):
    app.add_handler(
        MessageHandler(write_by_bot, filters.command("write") & filters.group)
    )
