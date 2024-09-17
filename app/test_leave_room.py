from fastapi.testclient import TestClient
from fastapi import status
from room import rooms

from main import app

client = TestClient(app)

# primero creamos una sala para testear la funcionalidad de salirse a una

rooms.ROOMS.append({"room_id":1, "room_name": "Room 1", 
                    "players_expected": 2, "players":["Braian"], "is_active": True })


# room 1

# test para asegurarse que un jugador puede unirse a una partida
def test_leave_room1():
    room_id = 1
    player_name = "Braian"
    expected_response = {"message": f"The player {player_name} has left the room {room_id}"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    print("PlayerList:")
    print(rooms.get_room_by_id(1)["players"])
    
# test: El jugador no existe en la partida
def test_leave_room2():
    room_id = 1 
    player_name = "Tadeo"
    
    expected_response = {"message": "There is not such a player"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    print(response)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    print(rooms.ROOMS) 
       
# test para sala inexistente
def test_leave_noroom():
    room_id = 2
    player_name = "Yamil"
    
    expected_response = {"message": "Room not found"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    print(response)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    
