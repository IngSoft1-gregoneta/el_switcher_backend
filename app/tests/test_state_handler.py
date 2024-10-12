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

def generate_test_match() -> List[MatchOut]:
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
    except:
        assert False, f"Creando mal matchs en db"
    return [match_1, match_2, match_3]

def test_add_states_of_differents_matches():
    reset()
    generate_test_room()
    matches = generate_test_match()
    add_parcial_match(matches[0])
    add_parcial_match(matches[0])
    add_parcial_match(matches[0])
    add_parcial_match(matches[1])
    add_parcial_match(matches[1])
    add_parcial_match(matches[0])
    add_parcial_match(matches[2])

    last_parcial_match1 = get_parcial_match(matches[0].match_id)
    assert last_parcial_match1.state == 3

    last_parcial_match2 = get_parcial_match(matches[1].match_id)
    assert last_parcial_match2.state == 1

    last_parcial_match3 = get_parcial_match(matches[2].match_id)
    assert last_parcial_match3.state == 0

    remove_last_parcial_match(matches[0].match_id)
    last_parcial_match1 = get_parcial_match(matches[0].match_id)
    assert last_parcial_match1.state == 2

    remove_last_parcial_match(matches[2].match_id)
    last_parcial_match2 = get_parcial_match(matches[2].match_id)
    assert last_parcial_match2 == None
