from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
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
            private=False,
            is_active=True,
        )
        roombd = Room(
            room_name=roomOut.room_name,
            room_id=str(roomOut.room_id),
            players_expected=roomOut.players_expected,
            owner_name=roomOut.owner_name,
            players_names=json.dumps(roomOut.players_names),
            private=roomOut.private,
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
    password = None
    payload = {"player_name": player_name, "password": password}
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        response = client.put(f"/rooms/join/{room_id}/{user_id}", json=payload)
        expected_response = True

        assert "Tito" in repo.get_room_by_id(room_id).players_names
        assert repo.get_room_by_id(room_id).room_id == room_id
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == expected_response


# test para asegurarse de que no haya duplicados de nombres de jugadores
def test_same_name():

    player_name = "Yamil"
    password = None
    payload = {"player_name": player_name, "password": password}

    user_id = uuid4()
    response = client.put(f"/rooms/join/{room_id}/{user_id}", json=payload)
    expected_response = {
        "detail": "Player name is already on the room, choose another name"
    }

    assert player_name in repo.get_room_by_id(room_id).players_names
    assert repo.get_room_by_id(room_id).room_id == room_id
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response


# test para que otro jugador se una a la misma partida
def test_join_room2():
    player_name = "Tadeo"
    password = None
    user_id = uuid4()
    payload = {"player_name": player_name, "password": password}

    with client.websocket_connect(f"/ws/{user_id}") as clientwebsocket:
        response = client.put(f"/rooms/join/{room_id}/{user_id}", json=payload)
        expected_response = expected_response = True

        assert repo.get_room_by_id(room_id).players_names == ["Yamil", "Tito", "Tadeo"]
        assert repo.get_room_by_id(room_id).room_id == room_id
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json() == expected_response


# test para evitar que otro jugador se una a una sala llena
def test_join_full_room():
    player_name = "Mou"
    password = None
    user_id = uuid4()

    payload = {"player_name": player_name, "password": password}

    expected_response = {"detail": "Room is full"}
    response = client.put(f"/rooms/join/{room_id}/{user_id}", json=payload)

    assert repo.get_room_by_id(room_id).players_names == ["Yamil", "Tito", "Tadeo"]
    assert repo.get_room_by_id(room_id).room_id == room_id
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == expected_response
    reset()


reset()
