from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from main import app,manager
from uuid import uuid4


client = TestClient(app)
uuid = uuid4()
repo = RoomRepository()

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd = Room(
                room_name="Room 1",
                room_id=1,
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
        match = MatchOut(
                match_id=1
            )
        repo_match.create_match(match)
    except:
        assert False, f"Creando mal match en db"

def test_leave_from_match_of_4_players():
    reset()
    generate_test_room()
    generate_test_match()
    room_id = 1
    player_name = "Braian"
    match = repo_match.get_match_by_id(room_id)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{uuid}")    
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in repo_match.get_match_by_id(room_id)
        data = websocket.receive_text()
        assert data == "LISTA"

def test_leave_from_match_of_3_players():
    room_id = 1
    player_name = "Tadeo"
    match = repo_match.get_match_by_id(room_id)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{uuid}")    
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in repo_match.get_match_by_id(room_id)
        data = websocket.receive_text()
        assert data == "LISTA"

def test_no_player_leave_from_match():
    room_id = 1
    player_name = "Tadeo" 
    user_id = uuid4()
    response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "user not found"}

def test_leave_from_no_match():
    room_id = 2
    player_name = "Facu"
    user_id = uuid4()
    response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "match not found"}

def test_leave_and_destroy_match():
    room_id = 1
    player_name = "Facu"
    with client.websocket_connect(f'/ws/{uuid}') as websocket:
        manager.bind_room(room_id,uuid)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{uuid}")    
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert repo_match.get_match_by_id(room_id) is None
        data = websocket.receive_text()
        assert data == "LISTA"
