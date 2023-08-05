import re
import datetime
import pandas as pd
from core import transactions
from database.sqlite_repository import Database

LIT_INVALID_INPUT = 'Invalid input. {}'


def add_transaction(database):
    while True:
        amount = input("Amount (max 3 decimals): ")
        try:
            amount = transactions.validate_amount(amount)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        description = input("Description: ")
        try:
            description = transactions.validate_description(description)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        recipient = input("Recipient (not empty): ")
        try:
            recipient = transactions.validate_recipient(recipient)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        date_input = input("Date (YYYY-MM-DD): ")
        try:
            date_input = transactions.validate_date(date_input)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        installment = input("Installment ([0]/1): ")
        try:
            installment = transactions.validate_installment(installment)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        category = input("Category (not empty): ")
        try:
            category = transactions.validate_category(category)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        priority = input("Priority ([(V)oluntary]/(N)eed/(M)andatory: ")
        try:
            priority = transactions.validate_priority(priority)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        automatic = input("Automatic ([0]/1): ")
        try:
            automatic = transactions.validate_automatic(automatic)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        method = input("Method (not empty): ")
        try:
            method = transactions.validate_method(method)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        account = input("Account (not empty): ")
        try:
            account = transactions.validate_account(account)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    while True:
        tags = input("Tags (semicolon delimiter): ")
        try:
            tags = transactions.validate_tags(tags)
            break
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))

    database.insert_transaction(amount, description, recipient, date_input, installment, category, priority, automatic,
                                method, account, tags)
    print("Success!")


def main():
    db = Database()
    db.initialize_database()

    while True:
        print("\nMenu:")
        print("1. Insert transaction")
        print("2. View all transactions")
        print("3. Delete transaction")
        print("0. Exit")

        choice = input("Scelta: ")

        if choice == "1":
            add_transaction(db)
        elif choice == "2":
            transactions = db.get_all_transactions(as_dataframe=True)
            pd.set_option('display.max_columns', None)
            print(transactions.to_string())
        elif choice == "3":
            id_row = input("ID: ")
            print("\tDeleting transaction with ID: {}".format(id_row))
            db.remove_transaction(id_row)
        elif choice == "0":
            print("Bye bye :)")
            db.close_connection()
            input("\n(press ENTER to close the window)")
            break
        else:
            print("Invalid option. Try again. :)")


if __name__ == "__main__":
    main()
