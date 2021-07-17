from util.database import DataConnector

from config.argsparser import ArgumentsParser
from entity.university import University

configs = ArgumentsParser()

class UniversityService:
    session = DataConnector.getSession(configs.db_host, configs.db_user, configs.db_password, configs.db_database)

    def addUniversity(self, id, name):
        university = University(id, name)
        self.session.add(university)
        self.session.commit()
        return university

    def getUniversityByName(self, name):
        our_univ = self.session.query(University).filter_by(name='Univ Of NY').first()
        return our_univ