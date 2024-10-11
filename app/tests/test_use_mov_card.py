from uuid import uuid1

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.match import *
from models.room import *

client = TestClient(app)

from models.match import *
from models.room import *

repo_room = RoomRepository()
repo_match = MatchRepository()

room1_id = uuid1()
room2_id = uuid1()
room3_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()
    manager.active_connections.clear()
    manager.rooms.clear()


def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
            room_name="Room 1",
            room_id=str(room1_id),
            players_expected=2,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo"]),
            is_active=True,
        )
        roombd2 = Room(
            room_name="Room 2",
            room_id=str(room2_id),
            players_expected=3,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil"]),
            is_active=True,
        )
        roombd3 = Room(
            room_name="Room 3",
            room_id=str(room3_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            is_active=True,
        )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.commit()
    finally:
        db.close()


def generate_test_match():
    try:
        match_1 = MatchOut(match_id=room1_id)
        match_2 = MatchOut(match_id=room2_id)
        match_3 = MatchOut(match_id=room3_id)
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
    except Exception as e:
        assert False, f"Creando mal matchs en db: {e}"

def test_use_mov_correct():
    reset()
    generate_test_room()
    generate_test_match()

    player_name = "Braian"
    match_id = room1_id

    response = client.put(f"/use_movement_card/{match_id}/{player_name}?card_index=0")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["visible_mov_cards"][0]["mov_status"] == "Played"
    reset()

def test_use_card_not_player_turn():
    reset()
    generate_test_room()
    generate_test_match()
    
    # Asigna un match al jugador Braian
    match_id = room1_id
    player_name = "Tadeo"
    
    
    response = client.put(f"/use_movement_card/{match_id}/{player_name}?card_index=0")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "It's not the player's turn"
    reset()

def test_use_card_invalid_index():
    reset()
    generate_test_room()
    generate_test_match()
    
    match_id = room1_id
    player_name = "Braian"

    
    response = client.put(f"/use_movement_card/{match_id}/{player_name}?card_index=10")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid card index"
    reset()


def test_use_card_no_cards_available():
    reset()
    generate_test_room()
    generate_test_match()
    
    match_id = room1_id
    player_name = "Braian"
    
    response = client.put(f"/use_movement_card/{match_id}/{player_name}?card_index=0")
    
    assert response.json()["detail"] == f"La carta seleccionada no está en la lista de mov_cards del jugador {player_name}."
    reset()