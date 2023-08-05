from database.sqlite_repository import Database
from ui.command_line import main_menu
from config.config import Config


def main():
    Config.get_instance().load_config()
    Database.get_instance().initialize_database()
    main_menu()
    Database.get_instance().close_connection()


if __name__ == "__main__":
    main()
