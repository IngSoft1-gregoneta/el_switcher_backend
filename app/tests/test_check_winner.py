from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.match import *
from models.room import *
from models.visible_match import *

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

# Ganador por descarte de mazo de cartas de figura
def test_check_winner_ok():
    reset()
    generate_test_room()
    generate_test_match_with_winner()

    match_id = room1_id
    player_name = "Braian"

    match = repo_match.get_match_by_id(match_id)
    add_parcial_match(match)

    expected_response = VisibleMatchData(match_id, player_name)
    
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room1_id, user_id)
        response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")
        assert response.status_code == status.HTTP_200_OK

    assert response.json() == expected_response.model_dump(mode="json")
    winner = match.get_player_by_name("Braian")
    assert expected_response.winner != winner
    reset()

# Ningun ganador
def test_check_winner_nobody():
    reset()
    generate_test_room()
    generate_test_match_without_winner()

    match_id = room2_id
    player_name = "Braian"

    match = repo_match.get_match_by_id(match_id)
    add_parcial_match(match)

    expected_response = VisibleMatchData(match_id, player_name)

    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room1_id, user_id)
        response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")
        assert response.status_code == status.HTTP_200_OK

    assert response.json() == expected_response.model_dump(mode="json")
    assert expected_response != None
    reset()

# Ganador por abandono del resto de jugadores
def test_check_winner_by_quitting():
    reset()
    generate_test_room()
    generate_test_match_without_winner()

    match_id = room2_id
    player_name = "Braian"

    match = repo_match.get_match_by_id(match_id)

    player2_name = "Tadeo"
    player3_name = "Yamil"
    player4_name = "Grego"

    # Sacamos a los 3 ultimos jugadores
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room2_id, user_id)
        response = client.put(f"/matchs/leave_match/{match_id}/{player4_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        updated_match = repo_match.get_match_by_id(match_id)
        assert updated_match.get_player_by_name(player4_name) == None
        data = Clientwebsocket.receive_text()
        assert data == "LISTA"
    
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room2_id, user_id)
        response = client.put(f"/matchs/leave_match/{match_id}/{player3_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        updated_match = repo_match.get_match_by_id(match_id)
        assert updated_match.get_player_by_name(player3_name) == None
        data = Clientwebsocket.receive_text()
        assert data == "LISTA"

    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room2_id, user_id)
        response = client.put(f"/matchs/leave_match/{match_id}/{player2_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        updated_match = repo_match.get_match_by_id(match_id)
        assert updated_match.get_player_by_name(player2_name) == None
        data = Clientwebsocket.receive_text()
        assert data == "LISTA"

    add_parcial_match(match)
    expected_response = VisibleMatchData(match_id, player_name)

    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room2_id, user_id)
        response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")
        assert response.status_code == status.HTTP_200_OK


    assert response.json() == expected_response.model_dump(mode="json")
    winner = match.get_player_by_name(player_name)
    assert expected_response.winner != winner
    reset()