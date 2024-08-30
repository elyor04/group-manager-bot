from pyrogram.dispatcher import Dispatcher
from pyrogram import Client, filters, types
from pyrogram.handlers import ChatMemberUpdatedHandler
from pyrogram.handlers.message_handler import MessageHandler


async def on_chat_member_updated(
    client: Client, chat_member_updated: types.ChatMemberUpdated
):
    new_member = chat_member_updated.new_chat_member
    old_member = chat_member_updated.old_chat_member

    if new_member and (not old_member):
        user = new_member.user
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

        await client.send_message(
            chat_member_updated.chat.id,
            f'Welcome to the group, <a href="tg://user?id={user.id}">{full_name}</a>',
        )


async def delete_join_leave_messages(client: Client, message: types.Message):
    await message.delete()


def register_member_handlers(dp: Dispatcher):
    dp.add_handler(
        ChatMemberUpdatedHandler(on_chat_member_updated, filters.group),
        0,
    )
    dp.add_handler(
        MessageHandler(
            delete_join_leave_messages,
            filters.group & (filters.new_chat_members | filters.left_chat_member),
        ),
        0,
    )
