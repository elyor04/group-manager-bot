import re
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

# Initialize Client
app = Client("my_bot", API_ID, API_HASH, bot_token=BOT_TOKEN, workdir="data")


async def extract_user_id(message_text: str):
    username_match = re.search(r"@\w+", message_text)
    username = username_match.group(0) if username_match else None

    if username:
        async with app:
            chat = await app.get_chat(username)
            return chat.id

    user_id_match = re.search(r"\b\d+\b", message_text)
    user_id = int(user_id_match.group(0)) if user_id_match else None

    return user_id
