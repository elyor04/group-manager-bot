import logging
import asyncio
from aiogram import Dispatcher
from app.database import initialize_db, close_db
from app.handlers import register_handlers
from app.middlewares import register_middlewares
from app.bot import bot
from app.client import client


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
