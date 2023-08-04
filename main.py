import datetime
import pandas as pd
from database.sqlite_repository import Database


def add_transaction(database):
    amount = float(input("Amount: "))
    description = input("Description: ")
    recipient = input("Recipient: ")
    date_input = input("Date (YYYY-MM-DD): ")
    installment = input("Installment: ")
    category = input("Category: ")
    priority = input("Priority: ")
    automatic = input("Automatic: ")
    method = input("Method: ")
    account = input("Account: ")
    tags = input("Tags (semicolon delimiter): ")

    if description == '':
        description = ''

    if date_input == '':
        date_input = datetime.date.today().strftime("%Y-%m-%d")

    if installment == '':
        installment = 0
    else:
        installment = int(installment)

    if priority == '':
        priority = 'Voluntary'

    if automatic == '':
        automatic = 0
    else:
        automatic = int(automatic)

    try:
        datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
    except ValueError:
        print("Data non valida. Utilizzare il formato YYYY-MM-DD.")
        return

    database.insert_transaction(amount, description, recipient, date_input, installment, category, priority, automatic, method, account, tags)
    print("Success!")


def main():
    db = Database()
    db.initialize_database()

    while True:
        print("\nMenu:")
        print("1. Aggiungi transazione")
        print("2. Visualizza transazioni")
        print("3. Rimuovi transazione")
        print("0. Esci")

        choice = input("Scelta: ")

        if choice == "1":
            add_transaction(db)
        elif choice == "2":
            transactions = db.get_all_transactions(as_dataframe=True)
            pd.set_option('display.max_columns', None)
            print(transactions.to_string())
        elif choice == "3":
            id_row = input("ID: ")
            db.remove_transaction(id_row)
        elif choice == "0":
            print("Ciao ciao :)")
            db.close_connection()
            break
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()
