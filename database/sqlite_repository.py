import sqlite3
import os
import pandas as pd
from config.config import Config


class Database:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._db_config = Config.get_instance().get_property('database')
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def _open_connection(self):
        db_file = self._db_config['file']
        db_directory = os.path.dirname(db_file)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()

    def _close_connection(self):
        self._connection.close()

    def execute_query_no_out(self, query, params=None):
        self._open_connection()

        if params is not None:
            self._cursor.execute(query, params)
        else:
            self._cursor.execute(query)

        self._connection.commit()

    def execute_create_no_out_from_file(self, file_path):
        with open(file_path, 'r') as file:
            scripts = file.read().split(';')
            for script in scripts:
                self.execute_query_no_out(script)

    def initialize_database(self):
        init_script = self._db_config['init_script']
        with open(init_script, 'r') as file:
            self._open_connection()
            self._cursor.executescript(file.read())
            self._connection.commit()
            self._close_connection()

        # self.execute_create_no_out_from_file(init_script)

    def execute_insert(self, table, values, columns=None):
        self._open_connection()
        question_list = ', '.join(['?' for _ in range(len(values))])
        if columns is None:
            query = 'INSERT INTO {} VALUES ({})'.format(table, question_list)
        else:
            column_list = ', '.join(columns)
            query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, column_list, question_list)
        self._cursor.execute(query, values)
        inserted_id = self._cursor.lastrowid
        self._connection.commit()
        self._close_connection()
        return inserted_id

    def execute_select(self, table, get_first=True, where=None, columns=None):
        self._open_connection()
        if columns is None:
            first_part = 'SELECT * FROM {}'.format(table)
        else:
            column_list = ', '.join(columns)
            first_part = 'SELECT {} FROM {}'.format(column_list, table)

        if where is None:
            second_part = ''
            query = '{} {}'.format(first_part, second_part)
            self._cursor.execute(query)
        else:
            keys, params = zip(*where.items())
            second_part = ' WHERE {}'.format(' AND '.join(['{}=?'.format(key) for key in keys]))
            query = '{} {}'.format(first_part, second_part)
            self._cursor.execute(query, params)

        if get_first:
            result = self._cursor.fetchone()
        else:
            result = self._cursor.fetchall()

        self._connection.commit()
        self._close_connection()
        return result

    def execute_delete(self, table, where=None):
        self._open_connection()
        if where is None:
            query = 'DELETE FROM {}'.format(table)
            self._cursor.execute(query)
        else:
            keys, params = zip(*where.items())
            query = 'DELETE FROM {} WHERE {}'.format(table, 'AND '.join(['{}=?'.format(key) for key in keys]))
            self._cursor.execute(query, params)
        self._connection.commit()
        self._close_connection()
