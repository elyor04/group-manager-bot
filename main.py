import logging
import asyncio
from aiogram import Dispatcher
from database import initialize_db, close_db
from handlers import register_handlers
from middlewares import register_middlewares
from bot import bot
from client import client


async def main():
    dp = Dispatcher()

    initialize_db()
    register_middlewares(dp)
    register_handlers(dp)

    await client.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    await client.stop()
    close_db()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
