from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from uuid import uuid4
import state_handler
from match_handler import MatchHandler
from main import app,manager
import figure_detector

from models.match import *
from models.room import * 

client = TestClient(app)
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
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
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

def test_initially_blocked_color_is_none():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    state_handler.add_parcial_match(match)
    assert match.board.blocked_color == TileColor.NONE.value

def test_blocked_color_change_on_discard():
    reset()
    user_id = uuid4()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    board = match.board
    card_index = x = y = 0
    player = match.players[0]
    player.fig_cards[0].fig_type = FigType.fige06.value
    for tile in board.tiles:
        tile.tile_color = TileColor.RED.value
    for i in range(4):
        board.tiles[i].tile_color = TileColor.BLUE.value
    match.board = figure_detector.figures_detector(board, [FigType.fige06.value])
    state_handler.add_parcial_match(match)
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id,user_id)
        response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None
        match_then = state_handler.get_parcial_match(room_id)
        assert match_then.board.blocked_color == TileColor.BLUE.value
    reset()

def test_blocked_color_change_on_block():
    reset()
    user_id = uuid4()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    board = match.board
    card_index = x = y = 0
    player = match.players[0]
    other_player = match.players[1]
    other_player.fig_cards[0].fig_type = FigType.fige06.value
    for tile in board.tiles:
        tile.tile_color = TileColor.RED.value
    for i in range(4):
        board.tiles[i].tile_color = TileColor.BLUE.value
    match.board = figure_detector.figures_detector(board, [FigType.fige06.value])
    state_handler.add_parcial_match(match)
    with client.websocket_connect(f"/ws/{user_id}") as Clientwebsocket:
        manager.bind_room(room_id,user_id)
        response = client.put(f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None
        match_then = state_handler.get_parcial_match(room_id)
        assert match_then.board.blocked_color == TileColor.BLUE.value
    reset()

def test_figure_detector_no_detect_fig_of_blocked_color():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    board = match.board
    board.blocked_color = TileColor.BLUE.value
    player = match.players[0]
    player.fig_cards[0].fig_type = FigType.fige06.value
    for tile in board.tiles:
        tile.tile_color = TileColor.RED.value
    for i in range(4):
        board.tiles[i].tile_color = TileColor.BLUE.value
    match.board = figure_detector.figures_detector(board, [FigType.fige06.value])
    state_handler.add_parcial_match(match)
    match_then = state_handler.get_parcial_match(room_id)
    for x in range(4):
        assert match_then.board.tiles[figure_detector.coordinates_to_index(x, 0)].tile_in_figure == FigType.none.value
    reset()