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
    user_id: int
    university_id: int
    course_id: int
    year: str
    admit_term: str
    area_of_specialization: str
    gre_score: str
    toefl_ielts_score: str

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                     nullable=False)
    name = db.Column(db.String)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    university_id = db.Column(db.Integer, db.ForeignKey('university.id', ondelete='CASCADE'),
                     nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'),
                     nullable=False)
    year = db.Column(db.String)
    admit_term = db.Column(db.String)
    area_of_specialization = db.Column(db.String)
    gre_score = db.Column(db.String)
    toefl_ielts_score = db.Column(db.String)

    def __repr__(self):
        return "<Application(name='%s', user_id='%s')>" % (self.name, self.user_id)