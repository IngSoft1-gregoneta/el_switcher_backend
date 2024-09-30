from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from models.match import *
from main import app

client = TestClient(app)

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

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
        roombd2 = Room(
                room_name="Room 2",
                room_id=2,
                players_expected=3,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil"]),
                is_active=True
            )
        roombd3 = Room(
                room_name="Room 3",
                room_id=3,
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Grego"]),
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
                match_id=1
            )
        match_2 = MatchOut(
                match_id=2
            )
        match_3 = MatchOut(
                match_id=3
            )
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
    except:
        assert False, f"Creando mal matchs en db"

def verify_test_ok(match_id):
    match = repo_match.get_match_by_id(match_id)
    assert match.players[0].has_turn
    assert not match.players[1].has_turn
    players_len = len(match.players)
    for i in range(len(match.players)):
        index = (i+1)%players_len
        response = client.put(f"/matchs/end_turn/{match_id}/{match.players[i].player_name}")
        assert response.status_code == status.HTTP_200_OK
        match = repo_match.get_match_by_id(match_id)
        for j in range(players_len):
            if match.players[index].player_name != match.players[j].player_name:
                assert not match.players[j].has_turn
        assert match.players[index].has_turn

def test_endturn_in_match_of_2_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 1
    verify_test_ok(match_id=match_id)
    reset()

def test_endturn_in_match_of_3_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 2
    verify_test_ok(match_id=match_id)
    reset()

def test_endturn_in_match_of_4_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 3
    verify_test_ok(match_id=match_id)
    reset()

def test_end_turn_no_match():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 4
    player_name = "Braian"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Match not found'}
    reset()

def test_end_turn_no_player():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 1
    player_name = "Yamil"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Player not found'}
    reset()

def test_end_turn_player_has_no_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = 1
    player_name = "Tadeo"
    response = client.put(f"/matchs/end_turn/{match_id}/{player_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Player has not the turn'}
    reset()