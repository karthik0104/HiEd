from flask_sqlalchemy import SQLAlchemy
from entrypoint import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
    __tablename__ = 'user'

    id: int
    public_id: str
    name: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return "<User(name='%s', public_id='%s')>" % (self.name, self.public_id)