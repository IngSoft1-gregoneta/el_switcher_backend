from config.repositorymanager import *
from sqlalchemy import (
    JSON,
    UUID,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

class Match(Base):
    __tablename__ = "Matches"
    match_id = Column(String(36), primary_key=True, index=True)
    board = Column(JSON)
    players = relationship("Player", back_populates="match")


class Room(Base):
    __tablename__ = "Rooms"
    room_id = Column(String(36), primary_key=True, index=True)
    room_name = Column(String(255))
    players_expected = Column(Integer)
    players_UUIDs = Column(JSON)
    owner_name = Column(String(255))
    players_names = Column(JSON)
    is_active = Column(Boolean)

class Playerdb(Base):
    __tablename__ = "Players"
    player_id = Column(UUID, primary_key=True,index=True)
    player_name = Column(String(255))
    mov_cards =  Column(JSON)
    fig_cards = Column(JSON)
    has_turn =  Column(Boolean)
    match_id = Column(String(36),ForeignKey('Matches.match_id'))
    match = relationship("Match", back_populates="players")


Base.metadata.create_all(bind=engine)