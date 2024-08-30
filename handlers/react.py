from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler
from utils.extractArgs import get_args

allowed_users = {
    # "-1002116123455": [7084938423],
    "all": [1398600688, 6840837015, 7084938423],
}


async def react_by_bot(client: Client, message: types.Message):
    user_id = message.from_user.id
    chat_id = str(message.chat.id)
    args_text = get_args(message.text)

    if (
        (user_id not in allowed_users["all"])
        and (user_id not in allowed_users.get(chat_id, []))
    ) or (not args_text):
        return

    await message.delete()
    if message.reply_to_message:
        await message.reply_to_message.react(args_text.split(maxsplit=1)[0])


def register_react_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(react_by_bot, filters.command("react") & filters.group), 0
    )
