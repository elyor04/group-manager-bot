from tortoise.models import Model
from tortoise import fields


class UserInfo(Model):
    id = fields.IntField(primary_key=True)

    chat_id = fields.IntField()
    user_id = fields.IntField()
    warnings = fields.IntField(default=0)
    muted = fields.IntField(default=0)
    banned = fields.IntField(default=0)
    messages = fields.IntField(default=0)

    class Meta:
        table = "UserInfos"

    def __repr__(self):
        return f"UserInfo(chat_id={self.chat_id}, user_id={self.user_id})"
