import logging
import asyncio
from app.database import initialize_db, close_db
from app.handlers import register_handlers
from app.middlewares import register_middlewares
from app.bot import bot, dp
from app.client import client
from app.utils.botCommands import botCommands


async def main():
    await initialize_db()
    register_middlewares(dp)
    register_handlers(dp)

    await client.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=botCommands)
    await dp.start_polling(bot)

    await client.stop()
    await close_db()


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
