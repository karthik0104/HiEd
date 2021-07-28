from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from entrypoint import db

@dataclass
class Course(db.Model):
    __tablename__ = 'course'

    id: int
    name: str
    university_id: int
    website: str
    address: str
    contact_number: str
    email: str
    acceptance_rate: float
    acceptance_rate_source: str
    quant_cutoff: int
    verbal_cutoff: int
    toefl_cutoff: int
    cutoff_score_source: str
    ranking: int
    ranking_source: str
    batch_size: int
    batch_size_source: str
    annual_fees: str
    annual_fees_source: str
    is_internship_mandatory: bool

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id', ondelete='CASCADE'), nullable=False)
    website = db.Column(db.String)
    address = db.Column(db.String)
    contact_number = db.Column(db.String)
    email = db.Column(db.String)
    acceptance_rate = db.Column(db.Float)
    acceptance_rate_source = db.Column(db.String)
    quant_cutoff = db.Column(db.Integer)
    verbal_cutoff = db.Column(db.Integer)
    toefl_cutoff = db.Column(db.Integer)
    cutoff_score_source = db.Column(db.String)
    ranking = db.Column(db.Integer)
    ranking_source = db.Column(db.String)
    batch_size = db.Column(db.Integer)
    batch_size_source = db.Column(db.String)
    annual_fees = db.Column(db.String)
    annual_fees_source = db.Column(db.String)
    is_internship_mandatory = db.Column(db.Boolean)

    def __repr__(self):
        return "<Course(name='%s')>" % (self.name)