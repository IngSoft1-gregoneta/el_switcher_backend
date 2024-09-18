from fastapi.testclient import TestClient
from fastapi import status
from room import *

from main import app

client = TestClient(app)

# primero creamos una sala para testear la funcionalidad de salirse a una
def TestRoom():
    ROOMS.clear()
    room_name = "Room 1"
    players_expected = 1
    owner_name = "Braian"
    roomOut = RoomOut(room_id=0,
                          room_name=room_name,
                          players_expected=players_expected,
                          players_names=[owner_name],
                          owner_name=owner_name,
                          is_active=True)
    ROOMS.append(roomOut.model_dump())

# room 1

# test: para asegurarse que un jugador puede unirse a una partida, devuelve HTTP200OK y mensaje advirtiendo
def test_leave_room1():
    TestRoom()
    room_id = 0
    player_name = "Braian"
    expected_response = {"message": f"The player {player_name} has left the room {room_id}"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert response.status_code == status.HTTP_200_OK
    assert player_name not in ROOMS[room_id]["players_names"]
    assert response.json() == expected_response
    
# test: El jugador no existe en la partida, devuelve http200OK pero mensaje advirtiendo
def test_leave_room2():
    TestRoom()
    room_id = 0
    player_name = "Tadeo"
    
    expected_response = {"message": "There is not such a player"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
       
# test: sala inexistente, devuelve HTTP200Ok y mensaje advirtiendo
def test_leave_noroom():
    TestRoom()
    room_id = 2
    player_name = "Yamil"
    
    expected_response = {"message": "Room not found"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    