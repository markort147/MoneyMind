import re
import datetime
import pandas as pd
from database.sqlite_repository import Database


def add_transaction(database):
    while True:
        amount = input("Amount (max 3 decimals): ")
        pattern = r'^[\d]*((\.[0-9]{0,3})|([0-9]{0,3}))$'
        if re.match(pattern, amount) is not None:
            amount = float(amount)
            print("\tInserted amount: {:.3f}".format(amount))
            break
        else:
            print("\tInvalid format!")

    description = input("Description: ")
    print("\tInserted description: {}".format(description))

    while True:
        recipient = input("Recipient (not empty): ")
        if recipient == '':
            print("\tInvalid recipient!")
        else:
            print("\tInserted recipient: {}".format(recipient))
            break

    while True:
        date_input = input("Date (YYYY-MM-DD): ")
        if date_input == '':
            date_input = datetime.date.today().strftime("%Y-%m-%d")
        try:
            datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
            print("\tInserted date: {}".format(date_input))
            break
        except ValueError:
            print("\tInvalid format!")

    while True:
        installment = input("Installment ([0]/1): ")

        if installment == '':
            installment = '0'

        if installment in ('0', '1'):
            installment = int(installment)
            print("\tInserted installment: {}".format(installment))
            break
        else:
            print("\tInvalid installment!")

    while True:
        category = input("Category (not empty): ")
        if category == '':
            print("\tInvalid category!")
        else:
            print("\tInserted category: {}".format(category))
            break

    while True:
        priority = input("Priority ([(V)oluntary]/(N)eed/(M)andatory: ")

        if priority in ('', 'V'):
            priority = 'Voluntary'
        elif priority == 'N':
            priority = 'Need'
        elif priority == 'M':
            priority = 'Mandatory'

        if priority in ('Voluntary', 'Need', 'Mandatory'):
            print("\tInserted priority: {}".format(priority))
            break
        else:
            print("\tInvalid priority!")

    while True:
        automatic = input("Automatic ([0]/1): ")

        if automatic == '':
            automatic = '0'

        if automatic in ('0', '1'):
            automatic = int(automatic)
            print("\tInserted automatic: {}".format(automatic))
            break
        else:
            print("\tInvalid automatic!")

    while True:
        method = input("Method (not empty): ")
        if method == '':
            print("\tInvalid method!")
        else:
            print("\tInserted method: {}".format(method))
            break

    while True:
        account = input("Account (not empty): ")
        if account == '':
            print("\tInvalid account!")
        else:
            print("\tInserted account: {}".format(account))
            break

    while True:
        tags = input("Tags (semicolon delimiter): ")
        pattern = r'^(|[\w]+|[\w]+(;[\w]+)*)$'
        if re.match(pattern, tags) is not None:
            print("\tInserted tags: {:.3f}".format(amount))
            break
        else:
            print("\tInvalid format!")

    database.insert_transaction(amount, description, recipient, date_input, installment, category, priority, automatic,
                                method, account, tags)
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
