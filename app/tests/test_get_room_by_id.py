from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from main import app
import json


client = TestClient(app)
repo = RoomRepository()

room1_id = uuid1()
noroom_id =uuid1()

def reset():
    repo.delete_rooms()

def generate_test_room():
    db = Session()
    try:
        players_expected = 2
        owner_name = "Braian"
        room1Out = RoomOut(room_id=room1_id,
                            room_name="Room 1",
                            players_expected=players_expected,
                            players_names=["Braian"],
                            owner_name=owner_name,
                            is_active=True)
        room1bd = Room(
                room_name=room1Out.room_name,
                room_id=str(room1Out.room_id),
                players_expected=room1Out.players_expected,
                owner_name=room1Out.owner_name,
                players_names=json.dumps(room1Out.players_names),
                is_active=True
            )
        db.add(room1bd)
        db.commit()
    finally:
        db.close()    


# test: para asegurarse de que no hay salas, devuelve HTTP200OK y lista vacia
def test_basic_get():
    reset()
    generate_test_room()
    response = client.get(f"/room/{room1_id}")
    assert response.status_code == status.HTTP_200_OK
    # Verificamos correctitud de la sala
    assert (response.json() == repo.get_room_by_id(room1_id).model_dump(mode = "json"))
    reset()
    
def test_noroom_get():
    reset()
    generate_test_room()
    response = client.get(f"/room/{noroom_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()


    
