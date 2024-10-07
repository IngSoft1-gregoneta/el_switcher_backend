from uuid import uuid4

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
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            is_active=True,
        )
        roombd2 = Room(
            room_name="Room 2",
            room_id=str(room2_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            is_active=True,
        )
        db.add(roombd1)
        db.add(roombd2)
        db.commit()
    finally:
        db.close()


def generate_test_match_with_winner():
    try:
        match_1 = MatchOut(match_id=room1_id)
        # Seteamos un jugador sin cartas de figura
        match_1.players[0].fig_cards = []
        repo_match.create_match(match_1)
    except:
        assert False, f"Partida no creada en db"


def generate_test_match_without_winner():
    try:
        match_2 = MatchOut(match_id=room2_id)
        repo_match.create_match(match_2)
    except:
        assert False, f"Partida no creada en db"


def test_check_winner_ok():
    reset()
    generate_test_room()
    generate_test_match_with_winner()

    match1_id = room1_id
    match = repo_match.get_match_by_id(match1_id)

    # Jugador sin cartas ==> winner
    expected_response = match.players[0].player_name

    response = client.get(f"/matchs/winner/{match1_id}")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == expected_response
    reset()

def test_check_winner_nobody():
    reset()
    generate_test_room()
    generate_test_match_without_winner()

    match2_id = room2_id

    expected_response = None

    response = client.get(f"/matchs/winner/{match2_id}")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == expected_response

    reset()