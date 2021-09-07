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
        self.security_keys_path = data['security']['app_keys_path']

        self.masterdata_folder = data['masterdata']['folder']
        self.university_course_file = data['masterdata']['university_course_file']
        self.locale_bundle_file = data['masterdata']['locale_bundle_file']
        self.plan_stages_metadata_file = data['masterdata']['plan_stages_metadata_file']

        self.rabbit_mq_connection_string = data['rabbitmq']['connection_string']
        self.rabbit_mq_socket_timeout = data['rabbitmq']['socket_timeout']
        self.rabbit_mq_routing_key = data['rabbitmq']['routing_key']

        self.redis_host = data['redis']['host']
        self.redis_port = data['redis']['port']
        self.redis_password = data['redis']['password']

        self.mongo_server = data['mongodb']['server']
        self.mongo_username = data['mongodb']['username']
        self.mongo_password = data['mongodb']['password']
        self.mongo_database = data['mongodb']['database']

