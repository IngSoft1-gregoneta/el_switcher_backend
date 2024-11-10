from uuid import uuid4

import figure_detector
import state_handler
from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.room import *

client = TestClient(app)
repo = RoomRepository()
from models.match import *
from models.room import *
from models.visible_match import VisibleMatchData

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()
not_room_id = uuid1()


def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()


def generate_test_room():
    db = Session()
    try:
        roombd = Room(
            room_name="Room 1",
            room_id=str(room_id),
            players_expected=2,
            owner_name="Braian",
            private=False,
            password=None,
            players_names=json.dumps(["Braian", "Tadeo"]),
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


def test_block_figure():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    user_id = uuid1()
    match = state_handler.get_parcial_match(room_id)
    for tile in match.board.tiles:
        tile.tile_color = TileColor.RED.value
    match.board.tiles[0].tile_color = TileColor.BLUE.value
    match.board.tiles[1].tile_color = TileColor.BLUE.value
    match.board.tiles[2].tile_color = TileColor.BLUE.value
    match.board.tiles[3].tile_color = TileColor.BLUE.value
    match.board = figure_detector.figures_detector(match.board, [FigType.fige06.value])
    init_board = match.board
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    other_player.fig_cards[0].fig_type = FigType.fige06.value
    card_index = 0
    x = 0
    y = 0
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room_id, user_id)
        response = client.put(
            f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == None
        # check db update
        after_discard_db_match = repo_match.get_match_by_id(room_id)
        other_player_then = after_discard_db_match.players[1]
        for i in range(25):
            if i == card_index:
                assert other_player_then.fig_cards[card_index].is_blocked
            else:
                assert not other_player_then.fig_cards[i].is_blocked
        # check reinit parcial states
        after_discard_match = state_handler.get_parcial_match(room_id)
        assert after_discard_match.state == 0
        other_player_then = after_discard_match.players[1]
        for i in range(25):
            if i == card_index:
                assert other_player_then.fig_cards[card_index].is_blocked
            else:
                assert not other_player_then.fig_cards[i].is_blocked
        # these changes should be not confirmed
        after_discard_match.board = Board()
        # check a player no got a new fig card after end turn if he has a blocked card his deck
        match = repo_match.get_match_by_id(room_id)
        player = match.players[0]
        player.fig_cards.remove(player.fig_cards[0])
        player.fig_cards[0].is_blocked = True
        repo_match.update_match(match)
        response = client.put(f"/matchs/end_turn/{room_id}/{player.player_name}")
        assert response.status_code == status.HTTP_200_OK
        after_end_turn_match = state_handler.get_parcial_match(room_id)
        assert after_end_turn_match.state == 0
        player_then = after_end_turn_match.players[0]
        visible_fig_cards_count = 0
        for fig_card in player_then.fig_cards:
            if fig_card.is_visible:
                visible_fig_cards_count += 1
        assert len(player_then.fig_cards) == 24
        assert visible_fig_cards_count == 2
        # check tiles after discard fig are the same color
        for i in range(36):
            assert (
                init_board.tiles[i].tile_color
                == after_end_turn_match.board.tiles[i].tile_color
            )


def test_initially_every_figures_are_unlocked():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    match = state_handler.get_parcial_match(room_id)
    for player in match.players:
        for fig_card in player.fig_cards:
            assert fig_card.is_blocked == False
    reset()


def test_match_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    card_index = 0
    x = 0
    y = 0
    response = client.put(
        f"/block_figure/{not_room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Match not found"}


def test_player_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    card_index = 0
    x = 0
    y = 0
    no_player_name = "Grego"
    other_player = match.get_player_by_name(match.players[1].player_name)
    response = client.put(
        f"/block_figure/{room_id}/{no_player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Player not found"}


def test_other_player_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    card_index = 0
    x = 0
    y = 0
    player = match.get_player_by_name(match.players[0].player_name)
    no_other_player_name = "Grego"
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{no_other_player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Other player not found"}


def test_player_no_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[1].player_name)
    other_player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    x = 0
    y = 0
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Player has not turn"}


def test_card_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    card_index = 25
    x = 0
    y = 0
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Card not found"}


def test_card_not_visible():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    card_index = 3
    x = 0
    y = 0
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Card is not visible"}


def test_fig_no_match():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    for tile in match.board.tiles:
        tile.tile_color = TileColor.RED.value
    match.board.tiles[0].tile_color = TileColor.BLUE.value
    match.board.tiles[1].tile_color = TileColor.BLUE.value
    match.board.tiles[2].tile_color = TileColor.BLUE.value
    match.board.tiles[3].tile_color = TileColor.BLUE.value
    match.board = figure_detector.figures_detector(match.board, [FigType.fige06.value])
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    other_player.fig_cards[0].fig_type = FigType.fig06.value
    card_index = 0
    x = 0
    y = 0
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Fig card not match with figure"}


def test_invalid_positions():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    card_index = 0
    x = 6
    y = 6
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid positions"}


def test_already_blocked_cards():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match1)

    match = state_handler.get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    other_player = match.get_player_by_name(match.players[1].player_name)
    card_index = 2
    x = 0
    y = 0
    other_player.fig_cards[card_index].is_blocked = True
    response = client.put(
        f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Other player already has blocked cards"}
    reset()

