from aiogram.types import User as AiogramUser

from loader import db


class User:
    def __init__(self,
                 user_id: int, first_name: str, last_name: str = '',
                 username: str = '', phone: str = '', email: str = '',
                 is_admin: bool = False, is_allowed: bool = False):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        self.email = email

        self.is_admin = is_admin
        self.is_allowed = is_allowed

    @property
    def full_name(self) -> str:
        """
        You can get full name of user.
        """
        full_name = self.first_name
        if self.last_name:
            full_name += ' ' + self.last_name
        return full_name

    @classmethod
    def get_from_aiogram_user(cls, user: AiogramUser, phone: str = '', email: str = '',
                              is_admin: bool = False, is_allowed: bool = False):
        """
        Creates an instance of User class from aiogram.User class
        """
        return cls(user_id=user.id, first_name=user.first_name, last_name=user.last_name, username=user.username,
                   phone=phone, email=email, is_admin=is_admin, is_allowed=is_allowed)

    @classmethod
    def get_from_database(cls, user_id: int):
        """
        Gets user from database by user_id
        """
        user_id, first_name, last_name, username, phone, email, is_admin, is_allowed = db.get_users(user_id=user_id)
        return cls(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                   phone=phone, email=email, is_admin=is_admin, is_allowed=is_allowed)
