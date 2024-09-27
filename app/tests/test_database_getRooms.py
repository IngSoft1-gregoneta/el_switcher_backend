from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from main import app


client = TestClient(app)
repo = RoomRepository()


def reset():
    repo.delete_rooms()

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

# test: para asegurarse de que no hay salas, devuelve HTTP200OK y lista vacia
def test_empty_rooms():
    reset()
    response = client.get("/rooms")    
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == []

def test_basic_get():
    reset()
    generate_test_room()
    response = client.get("/rooms")
    assert response.status_code == status.HTTP_200_OK
    # Check if room is correctly 
    assert response.json() == repo.get_rooms()
    reset()
    

reset()