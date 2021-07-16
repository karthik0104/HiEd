import json

config_file = 'config.json'

class ArgumentsParser:

    def __init__(self):
        data = json.load(config_file)

        self.db_host = data['database']['host']
        self.db_user = data['database']['user']
        self.db_password = data['database']['password']

