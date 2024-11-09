from uuid import uuid4
from fastapi.testclient import TestClient
from fastapi import status
from main import app, manager,match_handler
from models.match import *
from models.room import * 
from models.timer import *
import asyncio
import pytest

pytest_plugins = ('pytest_asyncio',)

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
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
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
    generate_test_match()
    
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        await asyncio.create_task(init_timer(room_id,1,manager,match_handler))
        data = Clientwebsocket.receive_text()
        assert data == "TIMER: STARTS 1"
        asyncio.sleep(2)
        data = Clientwebsocket.receive_text()
        assert data == "TIMER: FINISHED"
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"
        await stop_timer(room_id)
# Ejecuta el test