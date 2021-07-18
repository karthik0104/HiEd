from flask_sqlalchemy import SQLAlchemy
from entrypoint import db
from dataclasses import dataclass

@dataclass
class Application(db.Model):
    __tablename__ = 'application'

    id: int
    user_id: str
    name: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                     nullable=False)
    name = db.Column(db.String)

    user = db.relationship('User', backref='clients')

    def __repr__(self):
        return "<Application(name='%s', user_id='%s')>" % (self.name, self.user_id)