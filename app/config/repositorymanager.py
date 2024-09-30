import os
import uuid

from sqlalchemy import (
    JSON,
    UUID,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BDfilename = "../SwitcherDB.sqlite"
realdir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(realdir,BDfilename)}"


engine = create_engine(database_url, echo=False)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Match(Base):
    __tablename__ = "Matches"

    match_id = Column(String(36), primary_key=True, index=True)
    board = Column(JSON)
    players = Column(JSON)


class Room(Base):
    __tablename__ = "Rooms"
    room_id = Column(String(36), primary_key=True, index=True)
    room_name = Column(String(255))
    players_expected = Column(Integer)
    owner_name = Column(String(255))
    players_names = Column(JSON)
    is_active = Column(Boolean)


Base.metadata.create_all(bind=engine)
