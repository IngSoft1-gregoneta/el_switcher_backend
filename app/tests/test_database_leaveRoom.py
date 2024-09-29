from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app,manager
from models.room import *

client = TestClient(app)
uuid = uuid4()
repo = RoomRepository()


def reset():
    repo.delete_rooms()


def generate_test_room():
    db = Session()
    try:
        room_name = "Room 1"
        players_expected = 2
        owner_name = "Braian"
        roomOut = RoomOut(
            room_id=1,
            room_name=room_name,
            players_expected=players_expected,
            players_names=["Braian", "Yamil"],
            owner_name=owner_name,
            is_active=True,
        )
        roombd = Room(
            room_name=roomOut.room_name,
            room_id=roomOut.room_id,
            players_expected=roomOut.players_expected,
            owner_name=roomOut.owner_name,
            players_names=json.dumps(roomOut.players_names),
            is_active=True,
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
    player_name = "Yamil"
    expected_response = {
        "room_id": 1,
        "room_name": "Room 1",
        "players_expected": 2,
        "players_names": ["Braian"],
        "owner_name": "Braian",
        "is_active": True,
    }
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{uuid}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_name not in repo.get_room_by_id(room_id).players_names
        assert response.json() == expected_response
        data = websocket.receive_text()
        assert data == "LISTA"
    reset()


# test: El jugador no existe en la partida
def test_leave_room2():
    reset()
    generate_test_room()
    room_id = 1
    player_name = "Tadeo"
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{uuid}")
        assert player_name not in repo.get_room_by_id(room_id).players_names
        assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()


# test: sala inexistente
def test_leave_noroom():
    reset()
    generate_test_room()
    room_id = 2
    player_name = "Yamil"
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{uuid}")
        assert repo.get_room_by_id(room_id) == None
        assert response.status_code == status.HTTP_404_NOT_FOUND
    reset()


def test_owner_leave():
    reset()
    generate_test_room()
    room_id = 1
    player_name = "Braian"

    # Respuesta esperada cuando el propietario abandona la sala
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/rooms/leave/{room_id}/{player_name}/{uuid}")

    # Verificar que la sala ha sido eliminada
        assert repo.get_room_by_id(room_id) is None  # La sala debe estar eliminada

    # Verificar el mensaje de respuesta
        assert response.status_code == status.HTTP_202_ACCEPTED
        data = websocket.receive_text()
        assert data == "LISTA"

    reset()


reset()
