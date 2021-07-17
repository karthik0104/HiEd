from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id: int
    public_id: str
    name: str
    password: str

    id = Column(Integer, primary_key=True)
    public_id = Column(String)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', public_id='%s')>" % (self.name, self.public_id)