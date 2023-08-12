import yaml


class Config:
    _instance = None
    config_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def load_config(self):
        with open('./data/config.yaml', 'r') as file:
            self.config_data = yaml.safe_load(file)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def get_property(self, property_name, _data=None):
        if _data is None:
            data = self.config_data
        else:
            data = _data
        if '.' not in property_name:
            return data[property_name]
        else:
            keys = property_name.split('.')
            return self.get_property(property_name='.'.join(keys[1:]), _data=data[keys[0]])
