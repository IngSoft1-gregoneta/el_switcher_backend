from fastapi.testclient import TestClient
from fastapi import status
from room import rooms
from main import app

client = TestClient(app)

# Primero creamos las salas para testear la funcionalidad
rooms.ROOMS.append({"room_id": 1, "room_name": "Room 1", 
                    "players_expected": 4, "players": ["Braian", "Tadeo", "Yamil", "Grego"], 
                    "is_active": True, "creator": "Braian"})
rooms.ROOMS.append({"room_id": 2, "room_name": "Room 2", 
                    "players_expected": 2, "players": ["Braian", "Tadeo"], 
                    "is_active": True, "creator": "Braian"})

# Test para la Room 1, asegurando que "Braian" esté en la primera posición (más de 2 jugadores)
def test_sort_room1():
    room_id = 1
    expected_response = {"message": "Players sorted succesfuly"}
    
    # Hacemos la llamada al endpoint para ordenar los jugadores
    response = client.put(f"/rooms/randomize/?room_id={room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    
    # Aseguramos que "Braian" está en la primera posición
    sorted_players = rooms.get_room_by_id(room_id)["players"]
    assert sorted_players[0] == "Braian", "Braian should be the first player in the list"
    
    print("PlayerList after sorting:")
    print(sorted_players)

# Test para la Room 2, con 2 o menos jugadores, asegurando que "Braian" está en la primera posición
def test_sort_room2():
    room_id = 2
    
    expected_response = {"message": "Players sorted succesfuly"}
    
    response = client.put(f"/rooms/randomize/?room_id={room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    
    # Aseguramos que "Braian" está en la primera posición
    sorted_players = rooms.get_room_by_id(room_id)["players"]
    assert sorted_players[0] == "Braian", "Braian should be the first player in the list"
    
    print("PlayerList after sorting:")
    print(sorted_players)

# Test para una sala inexistente
def test_sort_nonexistent_room():
    room_id = 3
    expected_response = {"message": "Room not found"}
    
    response = client.put(f"/rooms/randomize/?room_id={room_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
