from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers.message_handler import MessageHandler


async def on_member_joined(client: Client, message: types.Message):
    await message.delete()

    for member in message.new_chat_members:
        full_name = f"{member.first_name or ''} {member.last_name or ''}".strip()
        await message.reply(
            f'Welcome to the group, <a href="tg://user?id={member.id}">{full_name}</a>'
        )


async def on_member_left(client: Client, message: types.Message):
    await message.delete()

    member = message.left_chat_member
    full_name = f"{member.first_name or ''} {member.last_name or ''}".strip()
    await message.reply(f'Goodbye, <a href="tg://user?id={member.id}">{full_name}</a>')


def register_member_handlers(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(on_member_joined, filters.group & filters.new_chat_members), 0
    )
    dp.add_handler(
        MessageHandler(on_member_left, filters.group & filters.left_chat_member), 0
    )
