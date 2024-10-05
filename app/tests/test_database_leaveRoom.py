from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.room import *

client = TestClient(app)
repo = RoomRepository()

room_id = uuid1()

def reset():
    repo.delete_rooms()
    manager.active_connections.clear()
    manager.rooms.clear()


def generate_test_room():
    db = Session()
    try:
        room_name = "Room 1"
        players_expected = 2
        owner_name = "Braian"
        roomOut = RoomOut(
            room_id=room_id,
            room_name=room_name,
            players_expected=players_expected,
            players_names=["Braian", "Yamil"],
            owner_name=owner_name,
            is_active=True,
        )
        roombd = Room(
            room_name=roomOut.room_name,
            room_id=str(roomOut.room_id),
            players_expected=roomOut.players_expected,
            owner_name=roomOut.owner_name,
            players_names=json.dumps(roomOut.players_names),
            is_active=True,
        )
        db.add(roombd)
        db.commit()
    finally:
        db.close()


# room 1


# test: para asegurarse que un jugador puede unirse a una partida, devuelve HTTP200OK y mensaje advirtiendo
def test_leave_room1():
    reset()
    generate_test_room()
    player_name = "Yamil"
    user_id = uuid4()
    expected_response = {
        "room_id": str(room_id),
        "room_name": "Room 1",
        "players_expected": 2,
        "players_names": ["Braian"],
        "owner_name": "Braian",
        "is_active": True,
    }
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_name not in repo.get_room_by_id(room_id).players_names
        assert response.json() == expected_response
        data = Clientwebsocket.receive_text()
        assert data == "LISTA"
    reset()


# test: El jugador no existe en la partida
def test_leave_room2():
    reset()
    generate_test_room()
    player_name = "Tadeo"
    user_id = uuid4()

    response = client.put(f"/rooms/leave/{room_id}/{player_name}/{user_id}")
    assert player_name not in repo.get_room_by_id(room_id).players_names
    assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()


# test: sala inexistente
def test_leave_noroom():
    reset()
    generate_test_room()
    room_id = uuid1()
    player_name = "Yamil"
    user_id = uuid4()

    response = client.put(f"/rooms/leave/{room_id}/{player_name}/{user_id}")
    assert repo.get_room_by_id(room_id) == None
    assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()


def test_owner_leave():
    reset()
    generate_test_room()
    player_name = "Braian"
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{user_id}")
        assert repo.get_room_by_id(room_id) is None
        assert response.status_code == status.HTTP_202_ACCEPTED
        data = Clientwebsocket.receive_text()
        assert data == "ROOM"

    reset()


reset()
