from fastapi import status
from fastapi.testclient import TestClient
from main import app, room_handler
from models.room import *

client = TestClient(app)
repo = RoomRepository()

room1_id = uuid1()
room2_id = uuid1()


def reset():
    repo.delete_rooms()


def generate_test_room():
    db = Session()
    try:
        players_expected = 2
        owner_name = "Braian"
        room1Out = RoomOut(
            room_id=room1_id,
            room_name="Room 1",
            players_expected=players_expected,
            players_names=["Braian"],
            owner_name=owner_name,
            private=False,
            is_active=True,
        )
        room2Out = RoomOut(
            room_id=room2_id,
            room_name="Room 2",
            players_expected=players_expected,
            players_names=["Braian"],
            private=False,
            owner_name=owner_name,
            is_active=True,
        )
        room1bd = Room(
            room_name=room1Out.room_name,
            room_id=str(room1Out.room_id),
            players_expected=room1Out.players_expected,
            owner_name=room1Out.owner_name,
            private=room1Out.private,
            players_names=json.dumps(room1Out.players_names),
            is_active=True,
        )
        room2bd = Room(
            room_name=room2Out.room_name,
            room_id=str(room2Out.room_id),
            players_expected=room2Out.players_expected,
            owner_name=room2Out.owner_name,
            players_names=json.dumps(room2Out.players_names),
            private=room1Out.private,
            is_active=True,
        )
        db.add(room1bd)
        db.add(room2bd)
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
    for i in range(2):
        assert str(repo.get_rooms()[i]["room_id"]) == response.json()[i]["room_id"]
        assert (
            repo.get_rooms()[i]["players_expected"]
            == response.json()[i]["players_expected"]
        )
        assert (
            repo.get_rooms()[i]["players_names"] == response.json()[i]["players_names"]
        )
        assert (
            str(repo.get_rooms()[i]["owner_name"]) == response.json()[i]["owner_name"]
        )
        assert repo.get_rooms()[i]["is_active"] == response.json()[i]["is_active"]
    reset()
