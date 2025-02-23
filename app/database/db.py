from tortoise import Tortoise
from app.config import TORTOISE_ORM


async def initialize_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
