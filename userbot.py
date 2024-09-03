from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "my_bot",
    API_ID,
    API_HASH,
    workdir="data",
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
)
