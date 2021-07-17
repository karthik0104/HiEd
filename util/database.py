from mysql.connector import connect, Error, OperationalError
from config.argsparser import ArgumentsParser
import cryptography
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity.university import University

configs = ArgumentsParser()

'''
DataConnector class which provides the base layer for interacting with the database and setting up connections.
'''
class DataConnector:
    session = None

    @classmethod
    def getSession(cls, host, user, password, database):
        if DataConnector.session is None:
            engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(configs.db_user,
                                                                            configs.db_password,
                                                                            configs.db_host,
                                                                            configs.db_database))
            engine.connect()

            # Create the session
            Session = sessionmaker(bind=engine)
            session = Session()

        return session

    def execute_test_script():
        try:
            with connect(
                    host=configs.db_host,
                    user=configs.db_user,
                    password=configs.db_password
            ) as connection:
                c = connection.cursor()

                fd = open('sql/test_sql.sql', 'r')
                sqlFile = fd.read()
                fd.close()

                sqlCommands = sqlFile.split(';')

                for command in sqlCommands:
                    try:
                        print(command)
                        c.execute(command)
                    except OperationalError as oe:
                        print(oe)
                print(connection)
        except Error as e:
            print(e)
