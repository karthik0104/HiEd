from util.database import DataConnector

from config.argsparser import ArgumentsParser
from entity.university import University
from sqlalchemy.orm import load_only

configs = ArgumentsParser()

class UniversityService:
    session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addUniversity(self, id, name):
        university = University(id, name)
        self.session.add(university)
        self.session.commit()
        return university

    def getUniversityById(self, id):
        our_univ = self.session.query(University.name.label('name')).filter_by(id=id).first()
        return our_univ._asdict()