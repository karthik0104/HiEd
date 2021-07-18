from config.argsparser import ArgumentsParser
from entity.application import Application
from entrypoint import db
from security.annotation import token_required

configs = ArgumentsParser()

class ApplicationService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addApplication(self, current_user, data):
        application = Application(name=data['name'], user=current_user)
        db.session.add(application)
        db.session.commit()
        return application