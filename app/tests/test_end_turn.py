from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from models.match import *
from typing import List
from main import app

from main import app

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
        if repo_room.get_room_by_id(1):
            repo_room.delete(1)
        if repo_match.get_match_by_id(1):
            repo_match.delete(1)

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=1,
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
        		)
        db.add(roombd1)
        db.commit()
    finally:
        db.close()

def test_endturn_correctness():
    reset()
    generate_test_room()

    try:
        match = MatchOut(match_id=1)
        assert match.match_id == 1
        repo_match.create_match(match)
        
        previous_turn = check_turn(match)
        next_turn(match)
        current_turn = check_turn(match)
        
        assert previous_turn != current_turn
        
    except ValueError as e:
        assert False, f"Error: {e}"
    finally:
        reset()

def test_endturn_cycle():
    reset()
    generate_test_room()

    try:
        match = MatchOut(match_id=1)
        assert match.match_id == 1
        repo_match.create_match(match)

        first_turn = check_turn(match)
        
        for _ in range(len(match.players)):    
            previous_turn = check_turn(match)
            next_turn(match)
            current_turn = check_turn(match)
            # Turn switches properly
            assert previous_turn != current_turn
            
        # Turn cycles properly
        last_turn = check_turn(match)

        assert first_turn == last_turn
        
    except ValueError as e:
        assert False, f"Error: {e}"
    finally:
        reset()
