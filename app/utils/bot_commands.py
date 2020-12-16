from aiogram import types


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("help", "help"),
            types.BotCommand("settings", "settings"),
        ]
    )
