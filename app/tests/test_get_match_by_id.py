from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from main import app

client = TestClient(app)
repo = RoomRepository()

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

room1_id = uuid1()
room2_id = uuid1()
room3_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=str(room1_id),
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        roombd2 = Room(
                room_name="Room 2",
                room_id=str(room2_id),
                players_expected=3,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil"]),
                is_active=True
            )
        roombd3 = Room(
                room_name="Room 3",
                room_id=str(room3_id),
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Mao"]),
                is_active=True
            )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match_1 = MatchOut(
                match_id=room1_id
            )
        match_2 = MatchOut(
                match_id=room2_id
            )
        match_3 = MatchOut(
                match_id=room3_id
            )
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
    except:
        assert False, f"Error al crear partidas en BD"

def test_get_match_1():
    reset()
    generate_test_room()
    generate_test_match()
    room_id = room1_id
    expected_match = repo_match.get_match_by_id(room_id).model_dump(mode="json")
    response = client.get(f"/matchs/{room_id}")    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_match
    reset()

def test_get_match_2():
    generate_test_room()
    generate_test_match()
    room_id = room2_id
    expected_match = repo_match.get_match_by_id(room_id).model_dump(mode="json")
    response = client.get(f"/matchs/{room_id}")    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_match
    reset()

def test_get_match_3():
    generate_test_room()
    generate_test_match()
    room_id = room3_id
    expected_match = repo_match.get_match_by_id(room_id).model_dump(mode="json")
    response = client.get(f"/matchs/{room_id}")    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_match
    reset()

def test_get_any_room():
    generate_test_room()
    generate_test_match()
    room_id = uuid1()
    response = client.get(f"/matchs/{room_id}")    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}
    reset()
