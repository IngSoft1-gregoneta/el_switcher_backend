from fastapi.testclient import TestClient
from fastapi import status
from main import app
from models.match import *
from models.room import * 

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
    for i in range(1,7):
        if repo_room.get_room_by_id(i):
            repo_room.delete(i)
        if repo_match.get_match_by_id(i):
            repo_match.delete(i)

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=1,
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        roombd2 = Room(
                room_name="Room 2",
                room_id=2,
                players_expected=3,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil"]),
                is_active=True
            )
        roombd3 = Room(
                room_name="Room 3",
                room_id=3,
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Mao"]),
                is_active=True
            )
        roombd4 = Room(
            room_name="Room 4",
            room_id=4,
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian","Tadeo","Yamil"]),
            is_active=True
        )
        roombd5 = Room(
            room_name="Room 5",
            room_id=5,
            players_expected=5,
            owner_name="Braian",
            players_names=json.dumps(["Braian","Tadeo","Yamil","Franco","Grego"]),
            is_active=True
        )
        roombd6 = Room(
            room_name="Room 6",
            room_id=6,
            players_expected=1,
            owner_name="Braian",
            players_names=json.dumps(["Braian"]),
            is_active=True
        )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.add(roombd4)
        db.add(roombd5)
        db.add(roombd6)
        db.commit()
    finally:
        db.close()    

def test_match_2_players():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=1)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == repo_match.get_match_by_id(matchIn.room_id).model_dump(mode="json")
    reset()

def test_match_3_players():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=2)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == repo_match.get_match_by_id(matchIn.room_id).model_dump(mode="json")
    reset()

def test_match_4_players():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=3)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == repo_match.get_match_by_id(matchIn.room_id).model_dump(mode="json")

def test_dup_match():
    matchIn = MatchIn(room_id=3)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There must be exactly one room per match'}

def test_no_full_match():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=4)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There must be exactly players expected amount of players'}
    reset()

def test_match_without_room():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=7)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There must be exactly one room per match'}
    reset()

def test_match_a_player():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=6)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There are not between 2 and 4 players'}
    reset()

def test_match_5_player():
    reset()
    generate_test_room()
    matchIn = MatchIn(room_id=5)
    response = client.post("/matchs/create_match", json=matchIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There are not between 2 and 4 players'}
    reset()