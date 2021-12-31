from flask_sqlalchemy import SQLAlchemy
import redis
from config.argsparser import ArgumentsParser

configs = ArgumentsParser()
REDIS_POOL = redis.ConnectionPool(host=configs.redis_host, port=configs.redis_port, password=configs.redis_password, decode_responses=True)
db = SQLAlchemy()