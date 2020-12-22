from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from models import User


class GetUserFromDB(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        data['user'] = User.get_from_database(message.from_user.id)