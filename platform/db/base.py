import os
from os.path import dirname
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///' + dirname(os.getcwd()) + '/db.sqlite3', echo=True)
Base = declarative_base()


class Images(Base):

    __tablename__ = "Photo"

    id = Column(Integer, primary_key=True)
    label = Column(String)

    def __init__(self, name):
        self.name = name


Base.metadata.create_all(engine)

