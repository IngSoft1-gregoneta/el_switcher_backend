from fastapi.testclient import TestClient
from fastapi import status
from room import rooms
from main import app

client = TestClient(app)

# función auxiliar para reinicializar las salas antes de cada test
def reset_rooms():
    rooms.ROOMS.clear()
    rooms.ROOMS.append({"room_id": 1, "room_name": "Room 1", 
                        "players_expected": 2, "players":[], "is_active": True })

    rooms.ROOMS.append({"room_id": 2, "room_name": "Room 2", 
                        "players_expected": 2, "players":[], "is_active": True })  

# test para asegurarse que un jugador puede unirse a una partida
def test_join_room1():
    reset_rooms()
    room_id = 1
    player_name = "Yamil"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para que otro jugador se una a la misma partida
def test_join_room2():
    room_id = 1 
    player_name = "Tadeo"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para evitar que otro jugador se una a una sala llena
def test_join_room3():
    room_id = 1    
    player_name = "Mou"
    
    expected_response = {"message": "Room is full"}
    
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para sala inexistente
def test_join_room4():
    reset_rooms()
    room_id = 3  # no existe
    player_name = "Yamil"
    
    expected_response = {"message": "Room not found"}
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response

# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_join_room5():
    reset_rooms()
    room_id = 2
    player_name = "Yamil"
    
    expected_response = {"message": f"The player {player_name} has joined the room {room_id}"}
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")  
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    assert len(rooms.ROOMS[1]["players"]) == 1  # Verifica que solo hay un jugador

# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_join_room6():
    reset_rooms()
    room_id = 2
    rooms.ROOMS[1]["players"] = ["Yamil"]  # simular que el jugador ya está en la sala
    
    player_name = "Yamil"
    expected_response = {"message": "The name already exists, choose another"}
    response = client.put(f"/rooms/join/?room_id={room_id}&player_name={player_name}")  
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response