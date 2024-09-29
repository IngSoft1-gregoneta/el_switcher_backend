from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from models.match import *
from typing import List
from main import app
from uuid import uuid4

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd = Room(
                room_name="Room 1",
                room_id=1,
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        db.add(roombd)
        db.commit()
    finally:
        db.close()

def generate_test_match():
    try:
        match = MatchOut(
                match_id=1
            )
        repo_match.create_match(match)
    except:
        assert False, f"Match mal creado"

def test_end_match_one_player():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 1

    match = repo_match.get_match_by_id(match_id)
    repo_match.delete_player("Tadeo", match_id)

    response = client.put(f"/matchs/end/{match_id}")
    assert response.status_code == status.HTTP_202_ACCEPTED

    assert response == match.players[0]
    reset()
    
