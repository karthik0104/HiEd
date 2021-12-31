from dataclasses import dataclass

from entrypoint import db
from datetime import datetime

@dataclass
class DiscussionGroup(db.Model):
    __tablename__ = 'discussion_group'

    id: int
    name: str
    description: str
    university_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    university_id = db.Column(db.String, db.ForeignKey('university.id', ondelete='CASCADE'), nullable=True,
                              primary_key=True)

    def __repr__(self):
        return "<DiscussionGroup(name='%s', description='%s')>" % (self.name, self.description)