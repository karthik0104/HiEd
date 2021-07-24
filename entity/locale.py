from dataclasses import dataclass
from entity.user import User
from entrypoint import db


@dataclass
class Locale(db.Model):
    __tablename__ = 'locale'

    id: int
    language: str

    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String)

    locale_fields = db.relationship('LocaleField', backref='locale')
    users = db.relationship('User', backref='locale')

    def __repr__(self):
        return "<Locale(language='%s')>" % (self.language)

@dataclass
class LocaleField(db.Model):
    __tablename__ = 'locale_bundle'

    id: int
    screen_name: str
    field_name: str
    locale_id: str
    value: str

    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String)
    field_name = db.Column(db.String)
    locale_id = db.Column(db.String, db.ForeignKey('locale.id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.String)

    def __repr__(self):
        return "<LocaleField(screen_name='%s', field_name='%s')>" % (self.screen_name, self.field_name)