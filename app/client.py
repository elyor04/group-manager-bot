from pyrogram import Client
from pyrogram.enums import ParseMode
from .utils.config import API_ID, API_HASH, BOT_TOKEN, DATA_DIR

client = Client(
    "bot",
    API_ID,
    API_HASH,
    workdir=DATA_DIR,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
)
