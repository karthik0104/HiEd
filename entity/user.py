from dataclasses import dataclass
from entity.application import Application

from entrypoint import db


@dataclass
class User(db.Model):
    __tablename__ = 'user'

    id: int
    public_id: str
    name: str
    password: str
    locale_id: int

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)
    locale_id = db.Column(db.Integer, db.ForeignKey('locale.id', ondelete='CASCADE'), nullable=True)

    applications = db.relationship('Application', backref='user')

    def __repr__(self):
        return "<User(name='%s', public_id='%s')>" % (self.name, self.public_id)