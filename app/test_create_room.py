from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)

def test_create_room1():
    room_name = "Room 1"
    players_expected = 2

    new_room_data = {
        "room_name": room_name,
        "players_expected": players_expected
    }
    response = client.post("/rooms/", json=new_room_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "room_id";"room_name";"players_expected"; "players"; "is_active" in response.json()
    assert response.json()["room_id"] == 1
    response.json()["room_name"] == room_name
    response.json()["players_expected"] == players_expected
    response.json()["players"] == []
    response.json()["is_active"] == True

def test_create_room2():
    room_name = "Room 2"
    players_expected = 3

    new_room_data = {
        "room_name": room_name,
        "players_expected": players_expected
    }
    response = client.post("/rooms/", json=new_room_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "room_id"; "room_name"; "players_expected"; "players"; "is_active" in response.json()
    assert response.json()["room_id"] == 2
    response.json()["room_name"] == room_name
    response.json()["players_expected"] == players_expected
    response.json()["players"] == []
    response.json()["is_active"] == True

def test_create_room3():
    room_name = "Room 1"
    players_expected = 3

    new_room_data = {
        "room_name": room_name,
        "players_expected": players_expected
    }
    response = client.post("/rooms/", json=new_room_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Room name already exists"
