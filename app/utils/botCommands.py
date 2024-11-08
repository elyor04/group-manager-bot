from aiogram.types import BotCommand

commands = [
    BotCommand(command="info", description="Info of a user"),
    BotCommand(command="warn", description="Warn a user"),
    BotCommand(command="mute", description="Mute a user"),
    BotCommand(command="ban", description="Ban a user"),
    BotCommand(command="unwarn", description="Unwarn a user"),
    BotCommand(command="unmute", description="Unmute a user"),
    BotCommand(command="unban", description="Unban a user"),
    BotCommand(command="write", description="Write a message"),
    BotCommand(command="delete", description="Delete a message"),
]
