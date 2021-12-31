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

    courses = db.relationship('Course', backref='university')
    discussion_groups = db.relationship('DiscussionGroup', backref='university')

    def __repr__(self):
        return "<University(name='%s')>" % (self.name)