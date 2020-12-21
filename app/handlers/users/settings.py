from aiogram import types
from aiogram.dispatcher.filters import CommandSettings

from app.loader import dp, db
from app.utils import logger


@dp.message_handler(CommandSettings())
async def command_settings_handler(msg: types.Message):
    logger.debug(f'Запрошена команда /settings от пользователя {msg.from_user.id} {msg.from_user.full_name}')
    if db.check_is_user_admin(msg.from_user.id):
        await msg.answer(f'Добро пожаловать, админ!')
    else:
        await msg.answer(f'Вы не являетесь администратором. Доступ к настройкам запрещён')