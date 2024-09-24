from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from main import app

client = TestClient(app)
repo = RoomRepository()

def reset():
    if repo.get_room_by_id(1):
        repo.delete(1)

def test_create_room_1_player():
    reset()
    room_name = "Room 2"
    players_expected = 1
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert repo.get_room_by_id(1) == None

def test_create_room_5_players():
    reset()
    room_name = "Room 3"
    players_expected = 5
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())  
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert repo.get_room_by_id(1) == None

def test_create_room_ok():
    reset()
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response not in repo.get_rooms()

def test_create_dup_room():
    
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Pepito"
    roomIn = RoomIn(room_name=room_name,
                     players_expected=players_expected,
                     owner_name=owner_name)
    response = client.post("/rooms/create_room", json=roomIn.model_dump())  
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert repo.get_room_by_id(2) == None
    reset()
reset()
    
    
