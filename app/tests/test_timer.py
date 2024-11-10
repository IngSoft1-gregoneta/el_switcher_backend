import asyncio
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager, match_handler
from models.match import *
from models.room import *
from models.timer import *

pytest_plugins = ("pytest_asyncio",)

repo_room = RoomRepository()
repo_match = MatchRepository()

client = TestClient(app)

room_id = uuid1()


def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()


def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
            room_name="Room 1",
            room_id=str(room_id),
            players_expected=2,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo"]),
            private=False,
            is_active=True,
        )
        db.add(roombd1)
        db.commit()
    finally:
        db.close()


def generate_test_match():
    try:
        match = MatchOut(match_id=room_id)
        repo_match.create_match(match)
    except:
        assert False, f"Creando mal match en db"


@pytest.mark.asyncio
async def test_timer():
    reset()
    generate_test_room()
    owner_name = "Braian"
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(room_id, player_id)
        response = client.post(f"/matchs/create_match/{room_id}/{owner_name}")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == repo_match.get_match_by_id(room_id).model_dump(
            mode="json"
        )
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
        data = Clientwebsocket.receive_text()
        assert "LISTA" in data
        data = Clientwebsocket.receive_text()
        assert "2024" in data

    reset()


# Ejecuta el test
