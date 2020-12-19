from aiogram.types import User as AiogramUser


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
    def from_aiogram_user(cls, user: AiogramUser):
        """
        Method creates class User from class aiogram.User
        """
        return cls(user_id=user.id, first_name=user.first_name,
                   last_name=user.last_name, username=user.username)
