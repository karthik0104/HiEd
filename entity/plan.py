from dataclasses import dataclass

from entrypoint import db
from datetime import datetime

@dataclass
class PlanStageMasterdata(db.Model):
    __tablename__ = 'plan_stage_masterdata'

    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return "<PlanStageMasterdata(name='%s', description='%s')>" % (self.name, self.description)


@dataclass
class Plan(db.Model):
    __tablename__ = 'plan'

    application_id: int
    plan_stage_id: str
    start_date: datetime
    end_date: datetime

    application_id = db.Column(db.Integer, db.ForeignKey('application.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    plan_stage_id = db.Column(db.Integer, db.ForeignKey('plan_stage_masterdata.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    start_date = db.Column(db.DateTime, server_default=db.func.now())
    end_date = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return "<Plan(application_id='%d', plan_stage_id='%d')>" % (self.application_id, self.plan_stage_id)