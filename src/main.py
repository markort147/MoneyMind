import datetime
from src.database.Database import Database


def add_transaction(database):
    amount = float(input("Importo: "))
    category = input("Categoria: ")
    payment_method = input("Mezzo di pagamento: ")
    date_str = input("Data (YYYY-MM-DD): ")
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Data non valida. Utilizzare il formato YYYY-MM-DD.")
        return

    database.insert_transaction(amount, category, payment_method, date)
    print("Transazione aggiunta con successo!")


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
        if choice == "2":
            transactions = db.get_all_transactions(as_dataframe=True)
            print(transactions)
        if choice == "3":
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
