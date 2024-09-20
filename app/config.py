import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

DATA_DIR = os.path.join(os.path.abspath("."), "data")
DB_PATH = os.path.join(DATA_DIR, "bot_data.db")

os.makedirs(DATA_DIR, exist_ok=True)
