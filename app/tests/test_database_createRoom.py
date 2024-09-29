from uuid import UUID, uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app
from models.room import *

client = TestClient(app)
uuid = uuid4()
repo = RoomRepository()


def reset():
    repo.delete_rooms()


def test_create_room_1_player():
    reset()
    room_name = "Room 2"
    players_expected = 1
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name, players_expected=players_expected, owner_name=owner_name
    )
    response = client.post(f"/rooms/create_room/{uuid}", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Wrong amount of players"}
    assert repo.get_room_by_id(1) == None
    reset()

def test_create_room_5_players():
    reset()
    room_name = "Room 3"
    players_expected = 5
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name, players_expected=players_expected, owner_name=owner_name
    )
    response = client.post(f"/rooms/create_room/{uuid}", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Wrong amount of players"}
    assert repo.get_room_by_id(1) == None
    reset()

def test_create_room_ok():
    reset()
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name, players_expected=players_expected, owner_name=owner_name
    )
    with client.websocket_connect(f"/ws/{uuid}"):
        response = client.post(f"/rooms/create_room/{uuid}", json=roomIn.model_dump())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() in repo.get_rooms()

def test_create_dup_room():
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(
        room_name=room_name, players_expected=players_expected, owner_name=owner_name
    )
    response = client.post(f"/rooms/create_room/{uuid}", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert repo.get_room_by_id(2) == None
    reset()

client.lifespan()