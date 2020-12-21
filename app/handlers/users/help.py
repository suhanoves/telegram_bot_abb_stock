from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from app.loader import dp, db
from utils import logger


@dp.message_handler(CommandHelp())
async def command_help_handler(msg: types.Message):
    logger.debug(f'Запрошена команда /help от пользователя {msg.from_user.id} {msg.from_user.full_name}')
    db.add_new_user(msg.from_user)
    await msg.answer(f'Отработка команды /help!')
