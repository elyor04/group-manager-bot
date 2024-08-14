from aiogram import Dispatcher, types


async def on_member_joined(message: types.Message):
    for member in message.new_chat_members:
        await message.answer(
            f'Welcome to the group, <a href="tg://user?id={member.id}">{member.full_name}</a>'
        )


async def on_member_left(message: types.Message):
    member = message.left_chat_member
    await message.answer(
        f'Goodbye, <a href="tg://user?id={member.id}">{member.full_name}</a>'
    )


def register_member_handlers(dp: Dispatcher):
    dp.register_message_handler(
        on_member_joined,
        content_types=types.ContentType.NEW_CHAT_MEMBERS,
    )
    dp.register_message_handler(
        on_member_left,
        content_types=types.ContentType.LEFT_CHAT_MEMBER,
    )
