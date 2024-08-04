from aiogram import Dispatcher, types


async def start_func(message: types.Message):
    user = message.from_user
    await message.answer(
        f'Hello <a href="tg://user?id={user.id}">{user.full_name}</a>\nAdd me to a group as an admin!'
    )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_func,
        commands=["start"],
        chat_type=[types.ChatType.PRIVATE],
    )
