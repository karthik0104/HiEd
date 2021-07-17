from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class University(Base):
    __tablename__ = 'university'

    id: int
    name: str

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<University(name='%s')>" % (self.name)