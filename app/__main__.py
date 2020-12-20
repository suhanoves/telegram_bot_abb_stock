from aiogram import Dispatcher
from aiogram.utils import executor

import utils
from app.loader import dp


async def on_startup(dispatcher: Dispatcher):
    await utils.setup_default_commands(dispatcher)


executor.start_polling(dp, on_startup=on_startup)
