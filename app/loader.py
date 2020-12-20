from aiogram import Bot, Dispatcher, types

from app.config import BOT_TOKEN
from database import Database

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

db = Database('database/database.sqlite')
