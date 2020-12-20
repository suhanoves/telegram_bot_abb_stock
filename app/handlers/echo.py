from aiogram.types import Message

from app.loader import dp


@dp.message_handler()
async def echo(msg: Message):
    await msg.answer(msg.text)
