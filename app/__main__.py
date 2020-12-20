from aiogram import Dispatcher
from aiogram.utils import executor

from app import handlers, filters, utils
from app.loader import dp, db


async def on_startup(dispatcher: Dispatcher):
    await utils.setup_default_commands(dispatcher)
    db.create_table_users()


executor.start_polling(dp, on_startup=on_startup)
