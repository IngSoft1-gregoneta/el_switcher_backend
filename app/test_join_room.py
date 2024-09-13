from fastapi.testclient import TestClient
from fastapi import status
from room import rooms

from main import app

client = TestClient(app)

# primero creamos algunas salas para testear la funcionalidad de unirse a una

rooms.ROOMS.append({"room_id":1, "room_name": "Room 1", 
                    "players_expected": 2, "players":[], "is_active": True })


# room 1

# test para asegurarse que un jugador puede unirse a una partida
def test_join_room1():
    room_id = 1
    player_name = "Yamil"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    print(rooms.ROOMS) 
    
# test para que otro jugador se una a la misma partida (que solo permite 2 jugadores)
def test_join_room2():
    room_id = 1 
    player_name = "Tadeo"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    print(rooms.ROOMS) 

# test para que otro jugador se una a la misma partida (que solo permite 2 jugadores)
# esta vez no deberia dejarlo entrar
def test_join_room3():
    room_id = 1
    player_name = "Mou"
    
    expected_response = {"message": "Room is full"}
    
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
       
# test para sala inexistente
def test_join_room4():
    room_id = 2
    player_name = "Yamil"
    
    expected_response = {"message": "Room not found"}
    
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    
