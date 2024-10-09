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

    board = figure_detector.figures_detector(match.board,['None'])
    
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            assert board.tiles[figure_detector.coordinates_to_index(x, y)].tile_in_figure == FigType.none.value

def test_fige01_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value

    board = figure_detector.figures_detector(match.board, 'fige01')
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige01.value

def test_fige01_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value

    board = figure_detector.figures_detector(match.board, ['fige01'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige01.value

def test_fige02_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige02'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige02.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige02.value

def test_fige03_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige03'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige03.value

def test_fige03_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fige03'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige03.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige03.value

def test_fige04_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige04'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fige04'])
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match.board, ['fige04'])

    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige04.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige04.value

def test_fige04_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match.board, ['fige04'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige05'])
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fige05'])

    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match.board, ['fige05'])

    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value

def test_fige05_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match.board, ['fige05'])

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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige06'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_in_figure == FigType.fige06.value

def test_fige06_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
        
    board = figure_detector.figures_detector(match.board, ['fige06'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige06.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige06.value

def test_fige07_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fige07'])
    
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_2_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fige07'])

    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_3_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match.board, ['fige07'])

    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value

def test_fige07_rot_4_detector():
    reset()
    generate_test_room()
    generate_test_match()

    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match.board, ['fige07'])

    assert board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value

def test_fig01_rot_1_detector():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig01','fige04','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fig01','fige04','fige05','fige07'])

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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    
    board = figure_detector.figures_detector(match.board, ['fig01','fige04','fige05','fige07'])

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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.GREEN.value
    
    board = figure_detector.figures_detector(match.board, ['fig01','fige04','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig02','fige03','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fig02','fige03','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig03','fige01','fige07'])
    
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

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fig03','fige01','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig04','fige01','fige03'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fig04','fige01','fige03'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig04','fige01','fige03'])
    
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

    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    
    board = figure_detector.figures_detector(match.board, ['fig04','fige01','fige03'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(4, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 4)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig06','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig06','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig06','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig06','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig07','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig07','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig07','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig07','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig08','fige07','fige06'])
 
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig08','fige07','fige06'])
 
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig08','fige07','fige06'])
 
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig08','fige07','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig09','fige04','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig09','fige04','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig09','fige04','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig09','fige04','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig10','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig10','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig11','fige04','fige05'])
     
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig11','fige04','fige05'])
     
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig11','fige04','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig11','fige04','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig12','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig12','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig13','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig13','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig13','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig13','fige05','fige06'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig14','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig14','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(3, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig14','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 3)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig14','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig15','fige02','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig15','fige02','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig15','fige02','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig15','fige02','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig16','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig16','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig16','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig16','fige05','fige07'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig17','fige04'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig18','fige02','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig18','fige02','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig18','fige02','fige05'])
    
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
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    
    board = figure_detector.figures_detector(match.board, ['fig18','fige02','fige05'])
    
    assert board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fig18.value
    assert board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fig18.value
