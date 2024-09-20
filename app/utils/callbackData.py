from aiogram.filters.callback_data import CallbackData


class MuteCallbackData(CallbackData, prefix="mute"):
    user_id: int
    action: str


class BanCallbackData(CallbackData, prefix="ban"):
    user_id: int
    action: str
