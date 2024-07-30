import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_PATH = os.environ.get("DB_PATH")
