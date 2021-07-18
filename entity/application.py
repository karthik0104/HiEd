from flask_sqlalchemy import SQLAlchemy
from entrypoint import db
from dataclasses import dataclass
import datetime

@dataclass
class Application(db.Model):
    __tablename__ = 'application'

    id: int
    name: str
    created_on: datetime
    updated_on: datetime

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                     nullable=False)
    name = db.Column(db.String)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    user = db.relationship('User', backref='users')

    def __repr__(self):
        return "<Application(name='%s', user_id='%s')>" % (self.name, self.user_id)