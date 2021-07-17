import json

config_file = 'config/config.json'

class ArgumentsParser:

    def __init__(self):
        f = open(config_file)
        data = json.load(f)

        self.db_host = data['database']['host']
        self.db_user = data['database']['user']
        self.db_password = data['database']['password']
        self.db_database = data['database']['database']

