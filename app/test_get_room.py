from fastapi.testclient import TestClient
from fastapi import status
from room import rooms 

from main import app

client = TestClient(app)

def test_basic():
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

def test_big_loop():
    i = 1
    while (i < 100):
        room_name = f"Room {i}"
        new_room_data = {"room name": room_name}
        rooms.ROOMS.append(new_room_data)

        response = client.get("/rooms/")
        assert response.status_code == status.HTTP_200_OK
        rooms_data = response.json()
        assert rooms_data[-1] == new_room_data
        assert rooms_data[i-1] == rooms.ROOMS[i-1]
        i += 1
        
def test_weird():
    room_name = "@!#./^"
    room_data = {"room name": room_name}
    rooms.ROOMS.append(room_data)
    
    response = client.get("/rooms/")    
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()

    assert rooms_data[-1] == room_data
    assert rooms_data[-1] == rooms.ROOMS[-1]

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
    rooms.ROOMS.append(new_room_data1)
    rooms.ROOMS.append(new_room_data2)

    response = client.get("/rooms/")
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()
    datalen = len(rooms_data)
    roomlen = len(rooms.ROOMS)
    assert datalen == roomlen

    assert rooms_data[-2] == new_room_data1
    assert rooms_data[-1] == new_room_data2

    assert rooms_data[-2]['room_name'] == room_name1
    assert rooms_data[-2]['players_expected'] == players_expected1
    assert rooms_data[-1]['room_name'] == room_name2
    assert rooms_data[-1]['players_expected'] == players_expected2

def test_large_get():
    response = client.get("rooms")
    assert response.status_code == status.HTTP_200_OK

    rooms_data = response.json()
    assert rooms_data == rooms.ROOMS