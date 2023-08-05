import sqlite3
import os
import pandas as pd
from config.config import Config


class Database:
    _instance = None
    _db_name = None
    _connection = None
    _cursor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.config = Config.get_instance()
            cls._instance._db_name = cls._instance.config.get_property('database')['file']
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def open_connection(self):
        db_directory = os.path.dirname(self._db_name)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        self._connection = sqlite3.connect(self._db_name)
        self._cursor = self._connection.cursor()

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()

    def execute_query_no_out(self, query, params=None):
        if self._cursor is None:
            self.open_connection()

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
        init_script = self.config.get_property('database')['init_script']
        self.execute_create_no_out_from_file(init_script)

    def insert_transaction(self, amount, description, recipient, date_input, installment, category, priority, automatic,
                           method, account, tags):
        if self._cursor is None:
            self.open_connection()

        # insert recipient
        query = 'SELECT id FROM recipients WHERE recipient_name = ?'
        params = (recipient,)
        self._cursor.execute(query, params)
        recipient_id = self._cursor.fetchone()
        if recipient_id is not None:
            recipient_id = recipient_id[0]
        else:
            query = 'INSERT INTO recipients (recipient_name) VALUES (?)'
            self._cursor.execute(query, params)
            recipient_id = self._cursor.lastrowid

        # insert category
        query = 'SELECT id FROM categories WHERE category_name = ?'
        params = (category,)
        self._cursor.execute(query, params)
        category_id = self._cursor.fetchone()
        if category_id is not None:
            category_id = category_id[0]
        else:
            query = 'INSERT INTO categories (category_name) VALUES (?)'
            self._cursor.execute(query, params)
            category_id = self._cursor.lastrowid

        # insert method
        query = 'SELECT id FROM methods WHERE method_name = ?'
        params = (method,)
        self._cursor.execute(query, params)
        method_id = self._cursor.fetchone()
        if method_id is not None:
            method_id = method_id[0]
        else:
            query = 'INSERT INTO methods (method_name) VALUES (?)'
            self._cursor.execute(query, params)
            method_id = self._cursor.lastrowid

        # insert account
        query = 'SELECT id FROM accounts WHERE account_name = ?'
        params = (account,)
        self._cursor.execute(query, params)
        account_id = self._cursor.fetchone()
        if account_id is not None:
            account_id = account_id[0]
        else:
            query = 'INSERT INTO accounts (account_name) VALUES (?)'
            self._cursor.execute(query, params)
            account_id = self._cursor.lastrowid

        # insert tags
        if len(tags) > 0:
            tags_list = tags.split(';')
            tag_id_list = []
            for tag in tags_list:
                query = 'SELECT id FROM tags WHERE tag_name = ?'
                params = (tag,)
                self._cursor.execute(query, params)
                tag_id = self._cursor.fetchone()
                if tag_id is not None:
                    tag_id = tag_id[0]
                else:
                    query = 'INSERT INTO tags (tag_name) VALUES (?)'
                    self._cursor.execute(query, params)
                    tag_id = self._cursor.lastrowid
                tag_id_list.append(str(tag_id))

        # insert transaction
        if len(tags) > 0:
            query = '''
                    INSERT INTO transactions (amount, description, recipient, date, installment, category, priority, automatic, method, account, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
            params = (
                amount, description, recipient_id, date_input, installment, category_id, priority, automatic, method_id,
                account_id, tags)
        else:
            query = '''
                    INSERT INTO transactions (amount, description, recipient, date, installment, category, priority, automatic, method, account)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
            params = (
                amount, description, recipient_id, date_input, installment, category_id, priority, automatic, method_id,
                account_id)
        print('params={}'.format(params))
        self.execute_query_no_out(query=query, params=params)
        transaction_id = self._cursor.lastrowid

        # insert transaction_tags
        if len(tags) > 0:
            for tag_id in tag_id_list:
                query = 'INSERT INTO transaction_tags (id_transaction, id_tag) VALUES (?, ?)'
                params = (transaction_id, int(tag_id))
                self._cursor.execute(query, params)

    def get_all_transactions(self, as_dataframe=False):
        if self._cursor is None:
            self.open_connection()

        query = 'SELECT * FROM transactions_view'
        self._cursor.execute(query)
        transactions = self._cursor.fetchall()

        if as_dataframe:
            return pd.DataFrame(data=transactions,
                                columns=["id", "amount", "description", "recipient", "date", "installment", "category",
                                         "priority", "automatic", "method", "account", "tags"])
        else:
            return transactions

    def remove_transaction(self, id_row):
        if self._cursor is None:
            self.open_connection()

        query = 'DELETE FROM transactions WHERE id=?'
        params = (int(id_row),)
        self.execute_query_no_out(query=query, params=params)
