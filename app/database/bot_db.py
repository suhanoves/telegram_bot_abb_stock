import sqlite3


class Database:

    def __new__(cls):
        """ singleton pattern implementation"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self, path_to_db='db.sqlite'):
        self.path_to_db = path_to_db

    def __enter__(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path_to_db)

    def __exit__(self: sqlite3.Connection, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.rollback()
        else:
            self.commit()
        self.close()

    def execute(self: sqlite3.Connection, sql: str, parameters: tuple = (),
                fetchone=False, fetchall=False, commit=False):
        cursor = self.cursor()
        cursor.execute(sql, parameters)

        data = None
        if commit:
            self.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        return data

    def create_table_users(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS Users(
                user_id INTEGER NOT NULL PRIMARY KEY,
                is_admin NUMERIC NOT NULL DEFAULT 0,
                is_allowed NUMERIC NOT NULL DEFAULT 0,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                username VARCHAR(255),
                phone VARCHAR(255),
                email VARCHAR(255)                
            )
        '''
        self.execute(sql=sql, commit=True)

    def add_user(self, user_id: int, is_admin: bool = False, is_allowed: bool = False, first_name: str = None,
                 last_name: str = None, username: str = None, phone: str = None, email: str = None):
        sql = 'INSERT INTO Users(user_id, name, phone, email) VALUES (?, ?, ?, ?)'
        parameters = user_id, is_admin, is_allowed, first_name, last_name, username, phone, email
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return self.execute(sql=sql, fetchall=True)

    @staticmethod
    def format_kwargs(sql, parameters: dict):
        formatted_sql = sql
        params = [f"{key} = ?" for key in parameters]
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