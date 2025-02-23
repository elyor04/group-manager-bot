from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.enums import ChatType, ContentType, ChatMemberStatus
from app.utils import welcome_template

router = Router()


@router.chat_member(
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def welcome_new_member(update: ChatMemberUpdated):
    new_member = update.new_chat_member
    old_member = update.old_chat_member

    if new_member and (new_member.status == ChatMemberStatus.MEMBER):
        user = new_member.user
        chat = update.chat

        if old_member and (old_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]):
            await update.bot.send_message(
                update.chat.id,
                welcome_template.format(user.id, user.full_name, str(chat.id)[4:], chat.title),
            )


@router.message(
    F.content_type.in_([ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER]),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]),
)
async def delete_join_leave_messages(message: Message):
    await message.delete()
