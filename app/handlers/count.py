from aiogram import Dispatcher, types, enums, F


async def count_messages(message: types.Message):
    pass


def register_count_handlers(dp: Dispatcher):
    dp.message.register(
        count_messages,
        F.chat.type.in_([enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]),
    )
