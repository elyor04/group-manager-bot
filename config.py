import os
from dotenv import load_dotenv

load_dotenv()

# Configuration settings
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
