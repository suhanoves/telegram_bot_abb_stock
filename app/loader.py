from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

from app.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
executor = Executor(dp)
