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

room1_id = uuid1()
room2_id = uuid1()
room3_id = uuid1()
room4_id = uuid1()

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
            is_active=True,
        )
        roombd2 = Room(
            room_name="Room 2",
            room_id=str(room2_id),
            players_expected=3,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil"]),
            is_active=True,
        )
        roombd3 = Room(
            room_name="Room 3",
            room_id=str(room3_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            is_active=True,
        )
        roombd4 = Room(
            room_name="Room 4",
            room_id=str(room4_id),
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian", "Tadeo", "Yamil", "Grego"]),
            is_active=True,
        )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.add(roombd4)
        db.commit()
    finally:
        db.close()


def generate_test_match():
    try:
        match_1 = MatchOut(match_id=room1_id)
        match_2 = MatchOut(match_id=room2_id)
        match_3 = MatchOut(match_id=room3_id)
        match_4 = MatchOut(match_id=room4_id)
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
        repo_match.create_match(match_4)
    except:
        assert False, f"Creando mal matchs en db"

def test_fige01_detector():
    reset()
    generate_test_room()
    generate_test_match()

    # rot 1
    match = repo_match.get_match_by_id(room1_id)
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_color = TileColor.BLUE.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.BLUE.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room1_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room1_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 2)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige01.value
    
    # rot 2
    match = repo_match.get_match_by_id(room2_id)
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room2_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room2_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 1)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige01.value

    # rot 3
    match = repo_match.get_match_by_id(room3_id)
    match.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.YELLOW.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.YELLOW.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room3_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room3_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 2)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 1)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige01.value

    # rot 4
    match = repo_match.get_match_by_id(room4_id)
    match.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_color = TileColor.RED.value
    match.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_color = TileColor.RED.value
    repo_match.update_match(match)

    match = repo_match.get_match_by_id(room4_id)
    figure_detector.figures_detector(match)
    match_out = repo_match.get_match_by_id(room4_id)
    
    assert match_out.board.tiles[figure_detector.coordinates_to_index(2, 0)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(1, 0)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 0)].tile_in_figure == FigType.fige01.value
    assert match_out.board.tiles[figure_detector.coordinates_to_index(0, 1)].tile_in_figure == FigType.fige01.value

    reset()