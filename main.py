import logging
from aiogram import executor
from bot import dp
from database.db import initialize_db, close_db
from handlers import register_handlers

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    initialize_db()
    register_handlers(dp)

    try:
        executor.start_polling(dp)
    finally:
        close_db()
