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

        self.token_validity_in_days = data['security']['token_validity_in_days']
        self.secret_key = data['security']['secret_key']

        self.masterdata_folder = data['masterdata']['folder']
        self.university_course_file = data['masterdata']['university_course_file']
        self.locale_bundle_file = data['masterdata']['locale_bundle_file']

