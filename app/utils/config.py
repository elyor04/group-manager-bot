import os
import time
from dotenv import load_dotenv

load_dotenv()
time.tzset()

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

DATA_DIR = os.path.join(os.path.abspath("."), "data")
os.makedirs(DATA_DIR, exist_ok=True)

TORTOISE_ORM = {
    "connections": {
        "default": f"sqlite://{os.path.join(DATA_DIR, "sqlite.db")}",
    },
    "apps": {
        "models": {
            # "models": ["app.database.models", "aerich.models"],
            "models": ["app.database.models"],
            "default_connection": "default",
        },
    },
}
