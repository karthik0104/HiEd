from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from entrypoint import db

@dataclass
class University(db.Model):
    __tablename__ = 'university'

    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "<University(name='%s')>" % (self.name)