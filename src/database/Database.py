import sqlite3
import os
import pandas as pd
from ..Config import Config

# todo creare una classe Transaction per gestire l'inserimento e l'estrazione di transaction

class Database:
    def __init__(self):
        self.config = Config.get_instance()
        self.db_name = self.config.get_database_file()
        self.connection = None
        self.cursor = None

    def open_connection(self):
        db_directory = os.path.dirname(self.db_name)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    def execute_query_no_out(self, query, params=None, from_file=False):
        if self.cursor is None:
            self.open_connection()

        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.connection.commit()

    def execute_create_no_out_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.execute_query_no_out(file.read())

    def initialize_database(self):
        tables = self.config.get_property('database')['tables']
        base_path = self.config.get_property('database')['scripts']
        for key, value in tables.items():
            self.execute_create_no_out_from_file(base_path + value['create_script'])

    def insert_transaction(self, amount, category, payment_method, date):
        # todo ampliare l'insert per tenere conto di tutte le colonne e delle foreign keys
        if self.cursor is None:
            self.open_connection()

        query = '''
                INSERT INTO transactions (amount, category, payment_method, date)
                VALUES (?, ?, ?, ?)
            '''
        params = (amount, category, payment_method, date)
        self.execute_query_no_out(query=query, params=params)

    def get_all_transactions(self, as_dataframe=False):
        if self.cursor is None:
            self.open_connection()

        query = 'SELECT * FROM transactions_view'
        transactions = self.cursor.fetchall()

        if as_dataframe:
            return pd.DataFrame(data=transactions, columns=["id", "amount", "category", "payment_method", "date"]).drop(
                columns=["id"])
        else:
            return transactions

    def remove_transaction(self, id_row):
        if self.cursor is None:
            self.open_connection()

        query = 'DELETE FROM transactions WHERE id=?'
        params = id
        self.execute_query_no_out(query=query, params=params)
