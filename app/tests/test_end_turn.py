from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.match import *
from models.room import *
from state_handler import *

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
            private=False,
            password=None,
            is_active=True,
        )
        roombd2 = Room(
            room_name="Room 2",
            room_id=str(room2_id),
            players_expected=3,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil"]),
            private=False,
            password=None,
            is_active=True,
        )
        roombd3 = Room(
            room_name="Room 3",
            room_id=str(room3_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            private=False,
            password=None,
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
    except:
        assert False, f"Creando mal matchs en db"


def verify_test_ok(match_id):
    match = repo_match.get_match_by_id(match_id)
    add_parcial_match(match)
    match = get_parcial_match(match_id)
    assert match.players[0].has_turn
    assert not match.players[1].has_turn
    assert match.state == 0
    players_len = len(match.players)
    player_id = uuid4()
    with client.websocket_connect(f"/ws/{player_id}") as Clientwebsocket:
        manager.bind_room(match_id, player_id)
        for i in range(len(match.players)):
            index = (i + 1) % players_len
            response = client.put(
                f"/matchs/end_turn/{match_id}/{match.players[i].player_name}"
            )
            assert response.status_code == status.HTTP_200_OK
            match = repo_match.get_match_by_id(match_id)
            assert match.state == 0
            for j in range(players_len):
                if match.players[index].player_name != match.players[j].player_name:
                    assert not match.players[j].has_turn
            assert match.players[index].has_turn
        data = Clientwebsocket.receive_text()
        assert data == "MATCH"


def test_endturn_in_match_of_2_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room1_id
    verify_test_ok(match_id=match_id)
    reset()


def test_endturn_in_match_of_3_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room2_id
    verify_test_ok(match_id=match_id)
    reset()


def test_endturn_in_match_of_4_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room3_id
    verify_test_ok(match_id=match_id)
    reset()


def test_end_turn_no_match():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = uuid1()
    player_name = "Braian"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Match not found"}
    reset()


def test_end_turn_no_player():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room1_id
    player_name = "Yamil"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Player not found"}
    reset()


def test_end_turn_player_has_no_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room1_id
    player_name = "Tadeo"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Player has not the turn"}
    reset()


# Si un jugador abandona la partida con turno, no deberia perderse
def test_end_turn_rotation_at_leaving_match():
    reset()
    generate_test_room()
    generate_test_match()

    match_id = room2_id
    player_name = "Braian"
    user_id = uuid4()

    # Eliminamos al primer jugador (ya que siempre posee el primer turno)
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room2_id, user_id)
        response = client.put(f"/matchs/leave_match/{match_id}/{player_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        updated_match = repo_match.get_match_by_id(match_id)
        assert updated_match.get_player_by_name(player_name) == None
        data = Clientwebsocket.receive_text()
        assert data == "LISTA"

    match = repo_match.get_match_by_id(match_id)

    player_with_turn = match.get_player_by_name("Tadeo")
    assert player_with_turn.has_turn
    reset()
