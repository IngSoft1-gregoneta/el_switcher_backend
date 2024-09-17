from fastapi.testclient import TestClient
from fastapi import status
from room import rooms 
from typing import List

from main import app

client = TestClient(app)

def test_basic():
    room_name = "Room 1"
    players_expected = 2
    players: List[str] = []

    new_room_data = {
        "room_name": room_name,
        "players_expected": players_expected
    }

    sent = client.post("/rooms/", json= new_room_data)
    assert sent.status_code == status.HTTP_201_CREATED

    response = client.get("/rooms/")
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()

    assert len(rooms_data) == 1
    assert rooms_data == new_room_data

def test_big_loop():
    i = 1
    while (i < 100):
        room_name = f"Room {i}"
        players_expected = 4
        new_room_data = {"room_name": room_name, 
                         "players_expected": players_expected}

        sent = client.post("/rooms/", json= new_room_data)
        assert sent.status_code == status.HTTP_201_CREATED

        response = client.get("/rooms/")
        assert response.status_code == status.HTTP_200_OK

        rooms_data = response.json()
        assert rooms_data[-1] == new_room_data
        i += 1
        
def test_weird():
    room_name = "@!#./^"
    players_expected = 4
    new_room_data = {"room_name": room_name,
                 "players_expected": players_expected}

    sent = client.post("/rooms/", json= new_room_data)
    assert sent.status_code == status.HTTP_201_CREATED
    
    response = client.get("/rooms/")    
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()

    assert rooms_data[-1] == new_room_data

def test_same_name():
    room_name1 = "Room 1"
    players_expected1 = 2

    room_name2 = "Room 1"
    players_expected2 = 2

    # rooms now have extra data
    new_room_data1 = {
        "room_name": room_name1,
        "players_expected": players_expected1
    }
    
    new_room_data2 = {
        "room_name": room_name2,
        "players_expected": players_expected2
    }

    sent1 = client.post("/rooms/", json= new_room_data1)
    assert sent1.status_code == status.HTTP_201_CREATED

    sent2 = client.post("/rooms/", json= new_room_data2)
    assert sent2.status_code == status.HTTP_201_CREATED

    response = client.get("/rooms/")
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()

    assert rooms_data[-2]['room_name'] == room_name1
    assert rooms_data[-2]['players_expected'] == players_expected1
    assert rooms_data[-1]['room_name'] == room_name2
    assert rooms_data[-1]['players_expected'] == players_expected2

def test_large_get():
    response = client.get("rooms")
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()
    assert rooms_data == rooms.ROOMS