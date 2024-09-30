from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import status
from main import app,manager
from models.match import *
from models.room import * 

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

def resetrooms():
    repo_room.delete_rooms()
def resetmatchs():
    repo_match.delete_matchs()
def resetmanager():
    manager.active_connections.clear()
    manager.rooms.clear()
def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=1,
                players_expected=2,
                players_names=json.dumps(["Braian","Tadeo"]),
                owner_name="Braian",
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

# test: para asegurarse que un jugador puede unirse a una partida, devuelve HTTP200OK y mensaje advirtiendo

def test_match_2_players():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=1
    match_in = MatchIn(room_id=room_id)
    owner_name="Braian"
    player_id = uuid4()
    with client.websocket_connect(f'/ws/{player_id}') as Clientwebsocket:
        manager.bind_room(room_id,player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
    resetrooms()
    resetmatchs()

def test_match_3_players():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=2
    match_in = MatchIn(room_id=room_id)
    owner_name="Braian"
    player_id = uuid4()
    with client.websocket_connect(f'/ws/{player_id}') as Clientwebsocket:
        manager.bind_room(room_id,player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
    resetrooms()
    resetmatchs()

def test_match4_players():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=3
    match_in = MatchIn(room_id=room_id)
    owner_name="Braian"
    player_id = uuid4()
    with client.websocket_connect(f'/ws/{player_id}') as Clientwebsocket:
        manager.bind_room(room_id,player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
    resetrooms()
#---

def test_dup_match():
    resetrooms()
    generate_test_room()
    room_id=3
    match_in = MatchIn(room_id=room_id)
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f'/ws/{player_id}') as Clientwebsocket:
        manager.bind_room(room_id,player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Bad request: There must be exactly one room per match'}
    resetrooms()
    resetmatchs()



def test_no_full_match():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=4
    match_in = MatchIn(room_id=room_id)
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There must be exactly players expected amount of players'}
    resetrooms()
    resetmatchs()

def test_match_5_player():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=5
    match_in = MatchIn(room_id=room_id)
    owner_name="Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There are not between 2 and 4 players'}
    resetrooms()
    resetmatchs()

def test_match_a_player():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=6
    match_in = MatchIn(room_id=room_id)
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Bad request: There are not between 2 and 4 players'}
    resetrooms()
    resetmatchs()

def test_match_without_room():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id=0
    match_in = MatchIn(room_id=room_id)
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Room not found'}
    resetrooms()
    resetmatchs()

def test_create_match_not_owner():
    resetrooms()
    resetmatchs()
    generate_test_room()
    room_id = 1
    match_in = MatchIn(room_id=room_id)
    owner_name = "Tadeo"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}", json=match_in.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Only the owner can create a match'}
    resetrooms()
    resetmatchs()