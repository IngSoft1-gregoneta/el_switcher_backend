from fastapi.testclient import TestClient
from fastapi import status
from room import rooms 

from main import app

client = TestClient(app)

def test_get_room1():
    room_name1 = "Room 1"
    players_expected1 = 2

    room_name2 = "Room 2"
    players_expected2 = 3

    new_room_data1 = {
        "room_name": room_name1,
        "players_expected": players_expected1
    }
    
    new_room_data2 = {
        "room_name": room_name2,
        "players_expected": players_expected2
    }
    rooms.ROOMS.append(new_room_data1)
    rooms.ROOMS.append(new_room_data2)

    response = client.get("/rooms/")

    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()

    assert len(rooms_data) == 2
    assert rooms_data[0] == rooms.ROOMS[0]
    assert rooms_data[1] == rooms.ROOMS[1]