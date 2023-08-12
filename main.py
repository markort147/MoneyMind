from database.sqlite_repository import Database
from ui.command_line import main_menu as cmd_main
from ui.dash_ui import home_page as dash_main
from config.config import Config

UI_MAPPING = {
    'cmd': cmd_main,
    'dash': dash_main
}


def main():
    Config.get_instance().load_config()
    Database.get_instance().initialize_database()

    ui = UI_MAPPING[Config.get_instance().get_property('ui')]
    ui.start()


if __name__ == "__main__":
    main()
