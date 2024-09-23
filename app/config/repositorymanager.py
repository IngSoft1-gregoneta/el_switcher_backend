import os

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON, create_engine, MetaData
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

BDfilename = "../SwitcherDB.sqlite"
realdir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(realdir,BDfilename)}"


engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class Match(Base):
    __tablename__ = "Matches"
    
    match_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer)
    board = Column(JSON)
    players = Column(JSON)

    
class Room(Base):
    __tablename__ = "Rooms"
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(255))
    players_expected = Column(Integer)
    owner_name =  Column(String(255))
    players_names = Column(JSON)
    is_active = Column(Boolean)
    
Base.metadata.create_all(bind=engine)





