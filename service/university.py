from config.argsparser import ArgumentsParser
from entity.university import University
from entrypoint import db

configs = ArgumentsParser()

class UniversityService:
    #session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addUniversity(self, current_user, data):
        university = University(data['name'])
        db.session.add(university)
        db.session.commit()
        return university

    def getUniversityById(self, current_user, id):
        our_univ = db.session.query(University.name.label('name')).filter_by(id=id).first()
        return our_univ._asdict()