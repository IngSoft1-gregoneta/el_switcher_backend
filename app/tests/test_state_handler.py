from fastapi.testclient import TestClient
from models.room import *
from state_handler import *

repo = RoomRepository()

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
    PARCIAL_MATCHES.clear()

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=str(room1_id),
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        roombd2 = Room(
                room_name="Room 2",
                room_id=str(room2_id),
                players_expected=3,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil"]),
                is_active=True
            )
        roombd3 = Room(
                room_name="Room 3",
                room_id=str(room3_id),
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Mao"]),
                is_active=True
            )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match_1 = MatchOut(
                match_id=room1_id
            )
        match_2 = MatchOut(
                match_id=room2_id
            )
        match_3 = MatchOut(
                match_id=room3_id
            )
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
    except:
        assert False, f"Creando mal matchs en db"

def test_add_get_remove_states_of_differents_matches():
    reset()
    generate_test_room()
    generate_test_match()
    
    match1 = repo_match.get_match_by_id(room1_id)
    match2 = repo_match.get_match_by_id(room2_id)
    match3 = repo_match.get_match_by_id(room3_id)

    add_parcial_match(match3)
    add_parcial_match(match1)
    add_parcial_match(match1)
    add_parcial_match(match1)
    add_parcial_match(match2)
    add_parcial_match(match2)
    add_parcial_match(match1)

    last_parcial_match1 = get_parcial_match(match1.match_id)
    assert last_parcial_match1.state == 3

    last_parcial_match2 = get_parcial_match(match2.match_id)
    assert last_parcial_match2.state == 1

    last_parcial_match3 = get_parcial_match(match3.match_id)
    assert last_parcial_match3.state == 0

    remove_last_parcial_match(match1.match_id)
    last_parcial_match1 = get_parcial_match(match1.match_id)
    assert last_parcial_match1.state == 2

    remove_last_parcial_match(match3.match_id)
    last_parcial_match2 = get_parcial_match(match3.match_id)
    assert last_parcial_match2 == None

def test_no_more_of_4_states_in_a_match():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room1_id)
    add_parcial_match(match1)
    add_parcial_match(match1)
    add_parcial_match(match1)
    add_parcial_match(match1)
    add_parcial_match(match1)
    last_parcial_match1 = get_parcial_match(match1.match_id)
    assert last_parcial_match1.state == 3
    reset()

