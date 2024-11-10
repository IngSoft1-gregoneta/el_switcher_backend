from fastapi.testclient import TestClient
from main import app
from uuid import uuid4
import json
from models.room import *
from main import app
from uuid import uuid4

client = TestClient(app)
repo = RoomRepository()

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd = Room(
                room_name="Room 1",
                room_id=str(room_id),
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Facu"]),
                is_active=True
            )
        db.add(roombd)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match = MatchOut(match_id=room_id)
        repo_match.create_match(match)
    except:
        assert False, f"Creando mal match en db"

async def test_chat_connection_and_message():
    reset()
    generate_test_room()
    generate_test_match()
    user_id = uuid4()
    async with client.websocket_connect(f"/websocket/chat/{user_id}") as websocket:
        test_message = "Hola, este es un mensaje de prueba"
        await websocket.send_text(test_message)

        response = await websocket.receive_text()
        data = json.loads(response)
        
        assert data["user_id"] == str(user_id)
        assert data["content"] == test_message
