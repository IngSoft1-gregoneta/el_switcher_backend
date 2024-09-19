from fastapi.testclient import TestClient
from fastapi import status
from room import *
from main import app


client = TestClient(app)
repo = RoomRepository()


def reset():
    if repo.get_room_by_id(1):
        repo.delete(1)

def generate_test_room():
    db = Session()
    try:
        room_name = "Room 1"
        players_expected = 2
        owner_name = "Braian"
        roomOut = RoomOut(room_id=1,
                            room_name=room_name,
                            players_expected=players_expected,
                            players_names=["Braian"],
                            owner_name=owner_name,
                            is_active=True)
        roombd = Room(
                room_name=roomOut.room_name,
                room_id=roomOut.room_id,
                players_expected=roomOut.players_expected,
                owner_name=roomOut.owner_name,
                players_names=json.dumps(roomOut.players_names),
                is_active=True
            )
        db.add(roombd)
        db.commit()
    finally:
        db.close()    

# room 1

# test: para asegurarse que un jugador puede unirse a una partida, devuelve HTTP200OK y mensaje advirtiendo
def test_leave_room1():
    reset()
    generate_test_room()
    room_id = 1
    player_name = "Braian"
    expected_response = {"message": f"The player {player_name} has left the room {room_id}"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert response.status_code == status.HTTP_200_OK
    assert player_name not in repo.get_room_by_id(room_id).players_names
    assert response.json() == expected_response
    reset()
# test: El jugador no existe en la partida, devuelve http200OK pero mensaje advirtiendo
def test_leave_room2():
    reset()
    generate_test_room()
    room_id = 1
    player_name = "Tadeo"
    
    expected_response = {"message": "There is not such a player"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    
    assert player_name not in repo.get_room_by_id(room_id).players_names
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    reset()   
# test: sala inexistente, devuelve HTTP200Ok y mensaje advirtiendo
def test_leave_noroom():
    reset()
    generate_test_room()
    room_id = 2
    player_name = "Yamil"
    
    expected_response = {"message": "Room not found"}
    
    response = client.put(f"/rooms/leave/?room_id={room_id}&player_name={player_name}")
    assert repo.get_room_by_id(room_id) == None
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
    reset()