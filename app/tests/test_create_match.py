from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.match import MatchRepository
from models.room import *

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()


def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def resetmanager():
    manager.active_connections.clear()
    manager.rooms.clear()

room1_id = uuid1()
room2_id = uuid1()
room3_id = uuid1()
room4_id = uuid1()
room5_id = uuid1()
room6_id = uuid1()

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
            room_name="Room 1",
            room_id=str(room1_id),
            players_expected=2,
            players_names=json.dumps(["Braian", "Tadeo"]),
            owner_name="Braian",
            is_active=True,
        )
        roombd2 = Room(
            room_name="Room 2",
            room_id=str(room2_id),
            players_expected=3,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil"]),
            is_active=True,
        )
        roombd3 = Room(
            room_name="Room 3",
            room_id=str(room3_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Mao"]),
            is_active=True,
        )
        roombd4 = Room(
            room_name="Room 4",
            room_id=str(room4_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil"]),
            is_active=True,
        )
        roombd5 = Room(
            room_name="Room 5",
            room_id=str(room5_id),
            players_expected=5,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Franco", "Grego"]),
            is_active=True,
        )
        roombd6 = Room(
            room_name="Room 6",
            room_id=str(room6_id),
            players_expected=1,
            owner_name="Braian",
            players_names=json.dumps(["Braian"]),
            is_active=True,
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
    reset()
    generate_test_room()
    room_id = room1_id
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(room_id, player_id)
        response = client.post(
            f"/matchs/create_match/{room_id}/{owner_name}"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
    reset()


def test_match_3_players():
    reset()
    generate_test_room()
    room_id = room2_id
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(room_id, player_id)
        response = client.post(
            f"/matchs/create_match/{room_id}/{owner_name}"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
    reset()


def test_match_4_players():
    reset()
    generate_test_room()
    room_id = room3_id
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(room_id, player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(mode="json")
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"


def test_dup_match():
    reset()
    generate_test_room()
    room_id = room3_id
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(room_id, player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Bad request: There must be exactly one room per match"}
    reset()


def test_no_full_match():
    reset()
    generate_test_room()
    room_id = room4_id
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Bad request: There must be exactly players expected amount of players"}
    reset()


def test_match_5_player():
    reset()
    generate_test_room()
    room_id = room5_id
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Bad request: There are not between 2 and 4 players"
    }
    reset()


def test_match_a_player():
    reset()
    generate_test_room()
    room_id = room6_id
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Bad request: There are not between 2 and 4 players"
    }
    reset()


def test_match_without_room():
    reset()
    generate_test_room()
    room_id = uuid1()
    owner_name = "Braian"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Room not found"}
    reset()


def test_create_match_not_owner():
    reset()
    generate_test_room()
    room_id = room1_id
    owner_name = "Tadeo"
    response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Only the owner can create a match"}
    reset()