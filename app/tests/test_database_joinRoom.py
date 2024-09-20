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
        players_expected = 3
        owner_name = "Yamil"
        roomOut = RoomOut(room_id=1,
                            room_name=room_name,
                            players_expected=players_expected,
                            players_names=["Yamil"],
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

# test para asegurarse que un jugador puede unirse a una partida
def test_join_room1():
    generate_test_room()
    room_id = 1
    player_name = "Tito"
    
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    expected_response = {"room_id": 1,
                         "room_name": "Room 1",
                         "players_expected": 3,
                         "players_names": ["Yamil", "Tito"],
                         "owner_name": "Yamil",
                         "is_active": True
                         }
    
    assert "Tito" in repo.get_room_by_id(room_id).players_names
    assert repo.get_room_by_id(room_id).room_id == 1
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == expected_response
    
# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_same_name():
    room_id = 1
    
    player_name = "Yamil"
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    expected_response = {"message": "The name already exists, choose another"} 
    
    assert player_name in repo.get_room_by_id(room_id).players_names
    assert repo.get_room_by_id(room_id).room_id == 1
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == expected_response

# test para que otro jugador se una a la misma partida
def test_join_room2():
    room_id = 1 
    player_name = "Tadeo"
    
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    expected_response =     expected_response = {"room_id": 1,
                         "room_name": "Room 1",
                         "players_expected": 3,
                         "players_names": ["Yamil", "Tito", "Tadeo"],
                         "owner_name": "Yamil",
                         "is_active": True
                         }
    
    assert repo.get_room_by_id(room_id).players_names == ["Yamil","Tito","Tadeo"]
    assert repo.get_room_by_id(room_id).room_id == 1
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == expected_response

# test para evitar que otro jugador se una a una sala llena
def test_join_full_room():
    room_id = 1    
    player_name = "Mou"
    
    expected_response = {"message": "Room is full"}
    response = client.put(f"/rooms/join?room_id={room_id}&player_name={player_name}")
    
    assert repo.get_room_by_id(room_id).players_names == ["Yamil","Tito","Tadeo"]
    assert repo.get_room_by_id(room_id).room_id == 1
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == expected_response
    reset()
reset()



