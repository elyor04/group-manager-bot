from aiogram import Dispatcher, types, enums, F
from aiogram.filters import Command


async def start_func(message: types.Message):
    user = message.from_user
    await message.answer(
        f'Hello, <a href="tg://user?id={user.id}">{user.full_name}</a>\nAdd me to a group as an admin!'
    )


def register_start_handlers(dp: Dispatcher):
    dp.message.register(
        start_func, Command("start"), F.chat.type == enums.ChatType.PRIVATE
    )
