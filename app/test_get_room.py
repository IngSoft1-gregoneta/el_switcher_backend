from fastapi.testclient import TestClient
from fastapi import status
from room import *
from typing import List

from main import app

client = TestClient(app)

def test_empty_rooms():
    
    response = client.get("/rooms/")    
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == []

def test_basic_get():

    room_name = "Room 1"
    players_expected = 2
    owner = "carlitos"

    new_room_data = RoomIn(
        room_name= room_name,
        players_expected = players_expected,
        owner_name = owner
    )
    
    sent = client.post("/rooms/create_room", json= new_room_data.model_dump() )
    assert sent.status_code == status.HTTP_201_CREATED
    # Check if room is correctly stored
    assert sent.json() in ROOMS

    response = client.get("/rooms/")
    assert response.status_code == status.HTTP_200_OK
    # Check if room is correctly 
    assert response.json() not in ROOMS
