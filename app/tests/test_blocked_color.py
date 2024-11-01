from fastapi import status
from models.room import *
from uuid import uuid4
import state_handler

repo = RoomRepository()

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd = Room(
                room_name="Room 1",
                room_id=str(room_id),
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Facu"]),
                is_active=True
            )
        db.add(roombd)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match = MatchOut(match_id=room_id)
        repo_match.create_match(match)
    except:
        assert False, f"Creando mal match en db"

def test_initially_blocked_color_is_none():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    reset()
    assert match.board.blocked_color == "None"