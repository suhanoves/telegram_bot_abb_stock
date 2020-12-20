from aiogram import types
from aiogram.dispatcher.filters import CommandSettings

from app.loader import dp, db
from utils import logger


@dp.message_handler(CommandSettings())
async def command_start_handler(msg: types.Message):
    logger.debug(f'Запрошена команда /settings от пользователя {msg.from_user.full_name}')
    db.add_new_user(msg.from_user)
    await msg.answer(f'Отработка команды /settings!')
