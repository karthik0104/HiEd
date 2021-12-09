from os import environ, path
from dotenv import load_dotenv
from config.argsparser import ArgumentsParser

configs = ArgumentsParser()

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    #SECRET_KEY = environ.get('SECRET_KEY')
    #FLASK_APP = environ.get('FLASK_APP')
    #FLASK_ENV = environ.get('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:3306/{3}'.format(configs.db_user,
                                                                            configs.db_password,
                                                                            configs.db_host,
                                                                            configs.db_database)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True