from pyrogram import Client
from pyrogram.enums import ParseMode
from database.db import initialize_db, close_db
from handlers import register_handlers
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "my_bot",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    workdir="data",
    parse_mode=ParseMode.HTML,
)


def start_bot():
    initialize_db()
    register_handlers(app)
    try:
        app.run()
    finally:
        close_db()
