from uuid import uuid4

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

def test_fige05_detector():
    reset()
    generate_test_room()
    generate_test_match()

    # fige05 rot 1
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value
    
    # fige05 rot 2
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige05.value

    # fige05 rot 3
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige05.value

    # fige05 rot 4
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige05.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige05.value

    reset()

def test_fige07_detector():
    reset()
    generate_test_room()
    generate_test_match()

    # fige07 rot 1
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value
    
    # fige07 rot 2
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value

    # fige07 rot 3
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value

    # fige07 rot 4
    match = repo_match.get_match_by_id(room_id)
    for x in range(figure_detector.columns):
        for y in range(figure_detector.columns):
            match.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.GREEN.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.GREEN.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige07.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige07.value