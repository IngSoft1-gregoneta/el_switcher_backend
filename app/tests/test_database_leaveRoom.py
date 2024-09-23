from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
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
    expected_response = {"room_id": 1,
                         "room_name": "Room 1",
                         "players_expected": 2,
                         "players_names": [],
                         "owner_name": "Braian",
                         "is_active": True
                         }
    
    response = client.put(f"/rooms/leave/{room_id}/{player_name}")
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert player_name not in repo.get_room_by_id(room_id).players_names
    assert response.json() == expected_response
    reset()
# test: El jugador no existe en la partida
def test_leave_room2():
    reset()
    generate_test_room()
    room_id = 1
    player_name = "Tadeo"
    
    
    response = client.put(f"/rooms/leave/{room_id}/{player_name}")
    
    assert player_name not in repo.get_room_by_id(room_id).players_names
    assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()   
# test: sala inexistente
def test_leave_noroom():
    reset()
    generate_test_room()
    room_id = 2
    player_name = "Yamil"
    
    
    response = client.put(f"/rooms/leave/{room_id}/{player_name}")
    assert repo.get_room_by_id(room_id) == None
    assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()
reset()