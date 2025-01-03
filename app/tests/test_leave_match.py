from uuid import uuid4

import state_handler
from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.room import *

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
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Facu"]),
            private=False,
            is_active=True,
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


def test_leave_from_match_of_4_players():
    reset()
    generate_test_room()
    generate_test_match()
    player_name = "Tadeo"
    user_id = uuid4()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in repo_match.get_match_by_id(room_id)
        matches_by_id: List[MatchOut] = [
            match
            for match in state_handler.PARCIAL_MATCHES
            if match.match_id == str(room_id)
        ]
        for match in matches_by_id:
            assert match.get_player_by_name("player_name") not in match
            for player in match.players:
                assert player.player_name != player_name


def test_leave_from_match_of_3_players():
    player_name = "Braian"
    user_id = uuid4()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in repo_match.get_match_by_id(room_id)
        matches_by_id: List[MatchOut] = [
            match
            for match in state_handler.PARCIAL_MATCHES
            if match.match_id == str(room_id)
        ]
        for match in matches_by_id:
            assert match.get_player_by_name("player_name") not in match
            for player in match.players:
                assert player.player_name != player_name


def test_leave_from_match_of_2_players():
    player_name = "Yamil"
    user_id = uuid4()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in repo_match.get_match_by_id(room_id)
        matches_by_id: List[MatchOut] = [
            match
            for match in state_handler.PARCIAL_MATCHES
            if match.match_id == str(room_id)
        ]
        for match in matches_by_id:
            assert match.get_player_by_name("player_name") not in match
            for player in match.players:
                assert player.player_name != player_name


def test_no_player_leave_from_match():
    player_name = "Tadeo"
    user_id = uuid4()
    response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Player not found"}


def test_leave_from_no_match():
    room_id = uuid1()
    player_name = "Facu"
    user_id = uuid4()
    response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Match not found"}


def test_leave_and_destroy_match_of_a_player():
    player_name = "Facu"
    user_id = uuid4()
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        assert repo_match.get_match_by_id(room_id) is None
        assert response.status_code == status.HTTP_202_ACCEPTED


def test_player_turn_leave_with_parcial_state():
    reset()
    generate_test_room()
    generate_test_match()
    player_name = "Braian"
    user_id = uuid4()
    match = repo_match.get_match_by_id(room_id)
    initial_board = copy.deepcopy(match.board)
    match.board = Board()
    state_handler.add_parcial_match(match)
    for player in match.players:
        if player.player_name == player_name:
            player_deleted = player
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        match = repo_match.get_match_by_id(room_id)
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert player_deleted not in match
        assert initial_board == match.board
        matches_by_id: List[MatchOut] = [
            match
            for match in state_handler.PARCIAL_MATCHES
            if match.match_id == str(room_id)
        ]
        for match in matches_by_id:
            assert match.get_player_by_name("player_name") not in match
            assert initial_board == match.board
            for player in match.players:
                assert player.player_name != player_name


reset()

