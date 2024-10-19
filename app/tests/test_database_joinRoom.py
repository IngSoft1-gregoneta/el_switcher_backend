from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app,manager
from models.room import *

client = TestClient(app)
repo = RoomRepository()

room_id = uuid1()

def reset():
    repo.delete_rooms()
    manager.active_connections.clear()
    manager.rooms.clear()

def generate_test_room():
    db = Session()
    try:
        room_name = "Room 1"
        players_expected = 3
        owner_name = "Yamil"
        roomOut = RoomOut(
            room_id=room_id,
            room_name=room_name,
            players_expected=players_expected,
            players_names=["Yamil"],
            owner_name=owner_name,
            is_active=True,
        )
        roombd = Room(
            room_name=roomOut.room_name,
            room_id=str(roomOut.room_id),
            players_expected=roomOut.players_expected,
            owner_name=roomOut.owner_name,
            players_names=json.dumps(roomOut.players_names),
            is_active=True,
        )
        db.add(roombd)
        db.commit()
    finally:
        db.close()


# test para asegurarse que un jugador puede unirse a una partida
def test_join_room1():
    reset()
    generate_test_room()
    player_name = "Tito"
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}"):
        response = client.put(f"/rooms/join/{room_id}/{player_name}/{user_id}")
        expected_response = {
            "room_id": str(room_id),
            "room_name": "Room 1",
            "players_expected": 3,
            "players_names": ["Yamil", "Tito"],
            "owner_name": "Yamil",
            "is_active": True,
        }

        assert "Tito" in repo.get_room_by_id(room_id).players_names
        assert repo.get_room_by_id(room_id).room_id == room_id
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == expected_response


# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_same_name():

    player_name = "Yamil"
    user_id = uuid4()
    response = client.put(f"/rooms/join/{room_id}/{player_name}/{user_id}")
    expected_response = {
        "detail": "Jugador con dicho nombre ya existente en la sala, elija otro"
    }

    assert player_name in repo.get_room_by_id(room_id).players_names
    assert repo.get_room_by_id(room_id).room_id == room_id
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response


# test para que otro jugador se una a la misma partida
def test_join_room2():
    player_name = "Tadeo"
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}"):
        response = client.put(f"/rooms/join/{room_id}/{player_name}/{user_id}")
        expected_response = expected_response = {
            "room_id": str(room_id),
            "room_name": "Room 1",
            "players_expected": 3,
            "players_names": ["Yamil", "Tito", "Tadeo"],
            "owner_name": "Yamil",
            "is_active": True,
        }

        assert repo.get_room_by_id(room_id).players_names == ["Yamil", "Tito", "Tadeo"]
        assert repo.get_room_by_id(room_id).room_id == room_id
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == expected_response


# test para evitar que otro jugador se una a una sala llena
def test_join_full_room():
    player_name = "Mou"
    user_id = uuid4()

    expected_response = {"detail": "Sala llena"}
    response = client.put(f"/rooms/join/{room_id}/{player_name}/{user_id}")

    assert repo.get_room_by_id(room_id).players_names == ["Yamil", "Tito", "Tadeo"]
    assert repo.get_room_by_id(room_id).room_id == room_id
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response
    reset()


reset()
