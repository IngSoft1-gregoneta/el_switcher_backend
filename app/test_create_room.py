from fastapi.testclient import TestClient
from fastapi import status
from room import *
from main import app

client = TestClient(app)

def test_create_room_ok():
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == ROOMS[0]
    print(response.json())


def test_create_room_1_player():
    room_name = "Room 2"
    players_expected = 1
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in ROOMS

def test_create_room_5_players():
    room_name = "Room 3"
    players_expected = 5
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())  
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in ROOMS

def test_create_dup_room():
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())  
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() not in ROOMS