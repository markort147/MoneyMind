import yaml


class Config:
    _instance = None
    config_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        with open('./data/config.yaml', 'r') as file:
            self.config_data = yaml.safe_load(file)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def get_property(self, property_name):
        return self.config_data[property_name]

    def get_database_file(self):
        return self.get_property('database')['file']
