from uuid import uuid4
import copy
from fastapi import status
from fastapi.testclient import TestClient
from main import app, manager
from models.match import *
from models.room import *
import figure_detector

client = TestClient(app)

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
        roombd1 = Room(
            room_name="Room 1",
            room_id=str(room_id),
            players_expected=2,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo"]),
            is_active=True,
        )
        db.add(roombd1)
        db.commit()
    finally:
        db.close()

def generate_test_match():
    try:
        match_1 = MatchOut(match_id=room_id)
        repo_match.create_match(match_1)
    except:
        assert False, f"Creando mal matchs en db"

def test_none_fig_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for i in range(len(match.players)):
        for j in range(len(match.players[i].fig_cards)):
            match.players[i].fig_cards[j].fig_type = FigType.none.value
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_in_figure = random.choice(list(FigType)).value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value

    board = figure_detector.figures_detector(match)
    
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            assert board.tiles[figure_detector.coordinates_to_index(x, y)].tile_in_figure == FigType.none.value

def test_fige01_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige01'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value

    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige01.value

def test_fige01_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige01'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value

    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige01.value

def test_fige02_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige02'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige02.value

def test_fige03_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige03'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige03.value

def test_fige03_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige03'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige03.value

def test_fige04_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige04'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige04'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige04'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match)

    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige04'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value

    reset()

def test_fige05_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match)

    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value

    reset()

def test_fige06_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fige06.value

def test_fige06_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige06.value

def test_fige07_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value

def test_fig01_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig01'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    match.players[1].fig_cards[0].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig01.value

def test_fig01_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig01'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    match.players[1].fig_cards[0].fig_type = 'fige07'   
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig01.value

def test_fig01_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig01'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    match.players[1].fig_cards[0].fig_type = 'fige07'   
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig01.value

def test_fig01_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig01'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    match.players[1].fig_cards[0].fig_type = 'fige07'   
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig01.value

    reset()

def test_fig02_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig02'
    match.players[0].fig_cards[1].fig_type = 'fige03'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig02.value

def test_fig02_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig02'
    match.players[0].fig_cards[1].fig_type = 'fige03'
    match.players[0].fig_cards[2].fig_type = 'fige05'

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig02.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig02.value

def test_fig03_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig03'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig03.value

def test_fig03_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig03'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige07'

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig03.value

def test_fig04_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig04'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige03'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig04.value

def test_fig04_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig04'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige03'

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig04.value

def test_fig04_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig04'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige03'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig04.value

def test_fig04_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig04'
    match.players[0].fig_cards[1].fig_type = 'fige01'
    match.players[0].fig_cards[2].fig_type = 'fige03'

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig04.value

def test_fig05_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig05'
    match.players[0].fig_cards[1].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(4, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(4, 0)].tile_in_figure == FigType.fig05.value

def test_fig05_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig05'
    match.players[0].fig_cards[1].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 4)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 4)].tile_in_figure == FigType.fig05.value

def test_fig06_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig06'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig06.value

def test_fig06_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig06'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig06.value

def test_fig06_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig06'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig06.value

def test_fig06_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig06'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig06.value

def test_fig07_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig07'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig07.value

def test_fig07_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig07'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig07.value

def test_fig07_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig07'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig07.value

def test_fig07_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig07'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig07.value

def test_fig08_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig08'
    match.players[0].fig_cards[1].fig_type = 'fige07'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig08.value

def test_fig08_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig08'
    match.players[0].fig_cards[1].fig_type = 'fige07'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig08.value

def test_fig08_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig08'
    match.players[0].fig_cards[1].fig_type = 'fige07'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig08.value

def test_fig08_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig08'
    match.players[0].fig_cards[1].fig_type = 'fige07'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig08.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig08.value

def test_fig09_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig09'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig09.value

def test_fig09_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig09'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig09.value

def test_fig09_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig09'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig09.value

def test_fig09_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig09'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig09.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig09.value

def test_fig10_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig10'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig10.value

def test_fig10_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig10'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig10.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig10.value

def test_fig11_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig11'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig11.value

def test_fig11_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig11'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig11.value

def test_fig11_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig11'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig11.value

def test_fig11_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig11'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig11.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig11.value

def test_fig12_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig12'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig12.value

def test_fig12_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig12'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig12.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig12.value

def test_fig13_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig13'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig13.value


def test_fig13_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig13'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig13.value

def test_fig13_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig13'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig13.value

def test_fig13_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig13'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige06'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig13.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig13.value

def test_fig14_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig14'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig14.value


def test_fig14_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig14'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig14.value

def test_fig14_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig14'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig14.value

def test_fig14_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig14'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig14.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig14.value

def test_fig15_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig15'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig15.value

def test_fig15_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig15'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig15.value

def test_fig15_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig15'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig15.value

def test_fig15_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig15'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig15.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig15.value

def test_fig16_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig16'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig16.value

def test_fig16_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig16'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig16.value

def test_fig16_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig16'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig16.value

def test_fig16_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig16'
    match.players[0].fig_cards[1].fig_type = 'fige05'
    match.players[0].fig_cards[2].fig_type = 'fige07'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig16.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig16.value

def test_fig17_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig17'
    match.players[0].fig_cards[1].fig_type = 'fige04'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig17.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig17.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig17.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig17.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig17.value

def test_fig18_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig18'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig18.value

def test_fig18_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig18'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig18.value

def test_fig18_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig18'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fig18.value

def test_fig18_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    match.players[0].fig_cards[0].fig_type = 'fig18'
    match.players[0].fig_cards[1].fig_type = 'fige02'
    match.players[0].fig_cards[2].fig_type = 'fige05'
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match)
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig18.value
