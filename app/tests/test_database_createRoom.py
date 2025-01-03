from uuid import UUID, uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.room import *

client = TestClient(app)
repo = RoomRepository()


def reset():
    repo.delete_rooms()


def resetmanager():
    manager.active_connections.clear()
    manager.rooms.clear()


def test_create_room_1_player():
    room_name = "Room 2"
    user_id = uuid4()
    players_expected = 1
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name,
        players_expected=players_expected,
        owner_name=owner_name,
        password=None,
    )
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        response = client.post(
            f"/rooms/create_room/{user_id}", json=roomIn.model_dump()
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Wrong amount of players"}
        assert repo.get_room_by_id(1) == None


def test_create_room_5_players():
    room_name = "Room 3"
    user_id = uuid4()
    players_expected = 5
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name,
        players_expected=players_expected,
        owner_name=owner_name,
        password=None,
    )
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        response = client.post(
            f"/rooms/create_room/{user_id}", json=roomIn.model_dump()
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Wrong amount of players"}
        assert repo.get_room_by_id(1) == None


def test_create_room_ok():
    room_name = "Room 1"
    user_id = uuid4()
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name,
        players_expected=players_expected,
        owner_name=owner_name,
        password=None,
    )
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        response = client.post(
            f"/rooms/create_room/{user_id}", json=roomIn.model_dump()
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response not in repo.get_rooms()


def test_create_dup_room():

    room_name = "Room 1"
    user_id = uuid4()
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name,
        players_expected=players_expected,
        owner_name=owner_name,
        password=None,
    )
    response = client.post(f"/rooms/create_room/{user_id}", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert repo.get_room_by_id(2) == None
    reset()
