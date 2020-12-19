import sqlite3
from typing import Union

from aiogram.types import User as AiogramUser

from models import User
from utils import logger


class Database:
    """
    A class used to represent a bot's database

    sqlite3 database class to create and connect the database
    This class create as a singleton for use only one copy through the project
    Has all function to manage bot's users and users search history.
    The database can also be opened manually with the open() method or as a context manager.

    Methods
    -------
    TODO add methods
    """

    def __new__(cls, database):
        """ singleton pattern implementation"""

        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self, database: str) -> None:
        """
        database : str - path to a database file
        """
        self.connection = None
        self.cursor = None

        if database:
            self.open(database)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(commit=True)

    def open(self, database: str) -> None:
        """
        Opens a connection to the SQLite database file *database*.

        This method allows to manually open a new database connection.
        It also calls from __init__ and with open class as a context manager

        database: str - path to a database file
        """
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            logger.info('Database connection successful')
        except sqlite3.Error:
            logger.error('Error connecting to database')

    def close(self, commit=False):
        """
        Closes a connection to the SQLite database

        This function manually closes the database connection.
        To commit database changes have to give explicitly-specified 'commit' argument
        Can also be closed like a context manager with commit changes.
        """

        if self.connection:
            if commit:
                self.connection.commit()
            self.cursor.close()
            self.cursor = None
            self.connection.close()
            self.connection = None

    def execute(self, query: str, parameters: tuple = (),
                fetchone: bool = False, fetchall: bool = False,
                commit: bool = False):
        """
        TODO add description
        """

        self.cursor.execute(query, parameters)

        data = None
        if commit:
            self.connection.commit()
        if fetchone:
            data = self.cursor.fetchone()
        if fetchall:
            data = self.cursor.fetchall()
        return data

    def create_table_users(self):
        query = '''
            CREATE TABLE IF NOT EXISTS Users(
                user_id INTEGER NOT NULL PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                username VARCHAR(255),
                phone VARCHAR(255),
                email VARCHAR(255),
                is_admin NUMERIC NOT NULL DEFAULT 0,
                is_allowed NUMERIC NOT NULL DEFAULT 0
            )
        '''
        self.execute(query=query, commit=True)

    def add_new_user(self, user: Union[AiogramUser, User], phone: str = '', email: str = '',
                     is_admin: bool = False, is_allowed: bool = False):

        if isinstance(user, AiogramUser):
            new_user = User.from_aiogram_user(user, phone, email, is_admin, is_allowed)
        else:
            new_user = user

        query = '''
                    INSERT OR IGNORE
                    INTO Users(user_id, first_name, last_name, username, phone, email, is_admin, is_allowed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
        parameters = (new_user.user_id, new_user.first_name, new_user.last_name, new_user.username,
                      new_user.phone, new_user.email, new_user.is_admin, new_user.is_allowed)

        self.execute(query=query, parameters=parameters, commit=True)

    # def select_all_users(self):
    #     sql = 'SELECT * FROM Users'
    #     return self.execute(sql=sql, fetchall=True)
    #
    # @staticmethod
    # def format_kwargs(sql, parameters: dict):
    #     formatted_sql = sql
    #     params = [f"{key} = ?" for key in parameters]
    #     formatted_sql += " AND ".join(params)
    #     return formatted_sql, tuple(parameters.values())
    #
    # def select_user(self, **kwargs):
    #     prefix_sql = 'SELECT * FROM Users WHERE '
    #     sql, parameters = self.format_kwargs(prefix_sql, kwargs)
    #     return self.execute(sql=sql, parameters=parameters, fetchone=True)
    #
    # def count_users(self):
    #     return self.execute('SELECT COUNT(*) FROM Users;', fetchone=True)
    #
    # def update_email(self, user_id, email):
    #     sql = 'UPDATE Users SET email=? WHERE user_id = ?'
    #     return self.execute(sql=sql, parameters=(email, user_id), commit=True)
    #
    # def delete_all_users(self):
    #     self.execute('DELETE FROM Users WHERE True', commit=True)
