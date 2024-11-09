from fastapi.testclient import TestClient
from main import app, manager
from models.room import *
from state_handler import *

repo = RoomRepository()

import switcher
from models.match import *
from models.room import *

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()
room2_id = uuid1()


def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()
    PARCIAL_MATCHES.clear()


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
        roombd2 = Room(
            room_name="Room 1",
            room_id=str(room2_id),
            players_expected=2,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo"]),
            private=False,
            is_active=True,
        )
        db.add(roombd2)
        db.commit()
    finally:
        db.close()


def generate_test_match():
    try:
        match_1 = MatchOut(match_id=room_id)
        match_2 = MatchOut(match_id=room2_id)
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
    except:
        assert False, f"Creando mal matchs en db"


def test_move_ok():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    user_id = uuid1()
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    card = player.mov_cards[card_index]
    x1 = 3
    y1 = 3
    x2 = x1 + card.vectors[0][0]
    y2 = y1 + card.vectors[0][1]
    while not switcher.is_valid_movement(card.mov_type, x1, y1, x2, y2):
        x1 = random.randrange(0, 5)
        x2 = random.randrange(0, 5)
        x2 = x1 + card.vectors[0][0]
        y2 = y1 + card.vectors[0][1]
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(
            f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}"
        )
        match = get_parcial_match(room_id)
        assert response.status_code == status.HTTP_200_OK
        assert match.state == 1


def test_move_used():
    user_id = uuid1()
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    card = player.mov_cards[card_index]
    x1 = 3
    y1 = 3
    x2 = x1 + card.vectors[0][0]
    y2 = y1 + card.vectors[0][1]
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(
            f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        expected_response = {"detail": "Card is used"}
        assert response.json() == expected_response


def test_Bad_move():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    user_id = uuid1()
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 2
    x1 = 3
    y1 = 3
    x2 = x1
    y2 = y1
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id, user_id)
        response = client.put(
            f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        expected_response = {"detail": "Invalid movement"}
        assert response.json() == expected_response


def test_match_doesnt_exist():
    reset()
    generate_test_room()
    generate_test_match()
    response = client.put(f"/parcial_move/{uuid1()}/{'tadeo'}/{3}/{5}/{6}/{7}/{8}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    expected_response = {"detail": "Match not found"}
    assert response.json() == expected_response


def test_player_doesnt_exist():
    reset()
    generate_test_room()
    generate_test_match()
    match2 = repo_match.get_match_by_id(room2_id)
    add_parcial_match(match2)
    response = client.put(f"/parcial_move/{room2_id}/{'Jorge'}/{3}/{5}/{6}/{7}/{8}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    expected_response = {"detail": "Player not found"}
    assert response.json() == expected_response


def test_player_doesnt_has_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match2 = repo_match.get_match_by_id(room2_id)
    add_parcial_match(match2)
    response = client.put(f"/parcial_move/{room2_id}/{'Tadeo'}/{3}/{5}/{6}/{7}/{8}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    expected_response = {"detail": "Player has not turn"}
    assert response.json() == expected_response


def test_player_bad_card():
    reset()
    generate_test_room()
    generate_test_match()
    match2 = repo_match.get_match_by_id(room2_id)
    add_parcial_match(match2)
    response = client.put(f"/parcial_move/{room2_id}/{'Braian'}/{7}/{5}/{6}/{7}/{8}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    expected_response = {"detail": "Card not found"}
    assert response.json() == expected_response

