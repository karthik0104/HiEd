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
    started_on: datetime
    updated_on: datetime
    completed_on: datetime

    application_id = db.Column(db.Integer, db.ForeignKey('application.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    plan_stage_id = db.Column(db.Integer, db.ForeignKey('plan_stage_masterdata.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    started_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now())
    completed_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return "<Plan(application_id='%d', plan_stage_id='%d')>" % (self.application_id, self.plan_stage_id)