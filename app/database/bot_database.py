import sqlite3

from app.utils import db_logger


class Database:
    def __init__(self, path_to_db='db.sqlite'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        connection.set_trace_callback(db_logger.debug)

        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS Users(
            user_id int NOT NULL PRIMARY KEY,
            name varchar(255) NOT NULL,
            phone varchar(255),
            email varchar(255)
            );
        '''
        self.execute(sql=sql, commit=True)

    def add_user(self, user_id: int, name: str, phone: str = None, email: str = None):
        sql = 'INSERT OR IGNORE INTO Users(user_id, name, phone, email) VALUES (?, ?, ?, ?)'
        parameters = user_id, name, phone, email
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return self.execute(sql=sql, fetchall=True)

    @staticmethod
    def format_kwargs(sql, parameters: dict):
        formatted_sql = sql
        params = [f"{item} = ?" for item in parameters]
        formatted_sql += " AND ".join(params)
        return formatted_sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        prefix_sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_kwargs(prefix_sql, kwargs)
        return self.execute(sql=sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute('SELECT COUNT(*) FROM Users;', fetchone=True)

    def update_email(self, user_id, email):
        sql = 'UPDATE Users SET email=? WHERE user_id = ?'
        return self.execute(sql=sql, parameters=(email, user_id), commit=True)

    def delete_all_users(self):
        self.execute('DELETE FROM Users WHERE True', commit=True)
