import pandas as pd
from core import transactions
from database.sqlite_repository import Database

LIT_INVALID_INPUT = 'Invalid input. {}.'


def main_menu():
    print("\n***Menu***")
    print()
    print("1. Insert transaction")
    print("2. View all transactions")
    print("3. Delete transaction")
    print("0. Exit")

    while True:
        choice = input("\nEnter your choice: ")

        if choice == "1":
            insert_transaction(last_view=main_menu)
        elif choice == "2":
            view_all_transactions(last_view=main_menu)
        elif choice == "3":
            delete_transaction(last_view=main_menu)
        elif choice == "0":
            print("See you next time!")
            input("\n(press ENTER to close the window)")
            return
        else:
            print("Invalid option!")


def delete_transaction(last_view):
    print("\n***Delete transaction***")
    print()
    id_row = input("Enter ID: ")
    Database.get_instance().remove_transaction(id_row)
    last_view()


def view_all_transactions(last_view):
    print("\n***All transactions***")
    print()
    transactions_df = Database.get_instance().get_all_transactions(as_dataframe=True)
    pd.set_option('display.max_columns', None)
    print(transactions_df.to_string())
    input("\nPress ENTER to go back")
    last_view()


def ask_for_input(prompt, validation_callable):
    while True:
        try:
            return validation_callable(input(prompt))
        except ValueError as e:
            print(LIT_INVALID_INPUT.format(e))


def insert_transaction(last_view):
    print("\n***Insert transaction***")
    print()

    description = ask_for_input("Description: ", transactions.validate_description)
    amount = ask_for_input("Amount (max 3 decimals): ", transactions.validate_amount)
    recipient = ask_for_input("Recipient (not empty): ", transactions.validate_recipient)
    date_input = ask_for_input("Date (YYYY-MM-DD): ", transactions.validate_date)
    category = ask_for_input("Category (not empty): ", transactions.validate_category)
    priority = ask_for_input("Priority ([(v)oluntary]/(n)eeded/(m)andatory): ", transactions.validate_priority)
    method = ask_for_input("Method (not empty): ", transactions.validate_method)
    account = ask_for_input("Account (not empty): ", transactions.validate_account)
    installment = ask_for_input("Installment ([0]/1): ", transactions.validate_installment)
    automatic = ask_for_input("Automatic ([0]/1): ", transactions.validate_automatic)
    tags = ask_for_input("Tags (semicolon delimiter): ", transactions.validate_tags)

    Database.get_instance().insert_transaction(amount, description, recipient, date_input, installment, category,
                                               priority, automatic,
                                               method, account, tags)

    last_view()
