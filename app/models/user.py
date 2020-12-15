from aiogram.types import User as AiogramUser


class User:
    def __init__(self, aiogram_user: AiogramUser,
                 is_admin: bool = False, is_allowed: bool = False,
                 phone: str = '', email: str = ''):
        self.id = aiogram_user.id
        self.is_admin = is_admin
        self.is_allowed = is_allowed
        self.first_name = aiogram_user.first_name
        self.last_name = aiogram_user.last_name
        self.username = aiogram_user.username
        self.phone = phone
        self.email = email
