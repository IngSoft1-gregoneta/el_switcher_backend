from fastapi.testclient import TestClient
from fastapi import status
from rooms import *
from main import app

client = TestClient(app)

def test_room():
    ROOMS.clear()
    room_name = "Room 1"
    players_expected = 2
    owner_name = "Yamil"
    roomOut = RoomOut(room_id=1,
                          room_name=room_name,
                          players_expected=players_expected,
                          players_names=[],
                          owner_name=owner_name,
                          is_active=True)
    ROOMS.append(roomOut.model_dump())

# test para asegurarse que un jugador puede unirse a una partida
def test_join_room1():
    test_room()
    room_id = 1
    player_name = "Yamil"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    
    assert ROOMS[0]["players_names"] == ["Yamil"]
    assert ROOMS[0]["room_id"] == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para que otro jugador se una a la misma partida
def test_join_room2():
    room_id = 1 
    player_name = "Tadeo"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    
    assert ROOMS[0]["players_names"] == ["Yamil", "Tadeo"]
    assert ROOMS[0]["room_id"] == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para evitar que otro jugador se una a una sala llena
def test_join_full_room():
    room_id = 1    
    player_name = "Mou"
    
    expected_response = {"message": "Room is full"}
    
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    
    assert ROOMS[0]["players_names"] == ["Yamil", "Tadeo"] # deberia seguir siendo esta la lista
    assert ROOMS[0]["room_id"] == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_same_name():
    test_room()
    room_id = 1
    ROOMS[0]["players_names"] = ["Yamil"]  # simular que el jugador ya está en la sala
    
    player_name = "Yamil"
    expected_response = {"message": "The name already exists, choose another"}
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")  
    
    assert ROOMS[0]["players_names"] == ["Yamil"] # no deberia dejar unir a otro jugador con el mismo nombre
    assert ROOMS[0]["room_id"] == 1
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response