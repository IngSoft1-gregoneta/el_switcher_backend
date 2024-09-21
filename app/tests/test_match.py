from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

def reset():
    for i in range(1,7):
        if repo_room.get_room_by_id(i):
            repo_room.delete(i)
        if repo_match.get_match_by_id(i):
            repo_match.delete(i)

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
                players_names=json.dumps(["Braian","Tadeo","Yamil","Mao"]),
                is_active=True
            )
        roombd4 = Room(
            room_name="Room 4",
            room_id=4,
            players_expected=4,
            owner_name="Braian",
            players_names=json.dumps(["Braian","Tadeo","Yamil"]),
            is_active=True
        )
        roombd5 = Room(
            room_name="Room 5",
            room_id=5,
            players_expected=5,
            owner_name="Braian",
            players_names=json.dumps(["Braian","Tadeo","Yamil","Franco","Grego"]),
            is_active=True
        )
        roombd6 = Room(
            room_name="Room 6",
            room_id=6,
            players_expected=1,
            owner_name="Braian",
            players_names=json.dumps(["Braian"]),
            is_active=True
        )
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.add(roombd4)
        db.add(roombd5)
        db.add(roombd6)
        db.commit()
    finally:
        db.close()    

def test_match_2_players():
    reset()
    generate_test_room()
    try:
        match = MatchOut(match_id = 1)
        has_turn_count = 0
        assert match.match_id == 1
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 25, f"expected 50 fig cards between 2 players (25), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"
    finally:
        reset()

def test_match_3_players():
    reset()
    generate_test_room()
    has_turn_count = 0
    try:
        match = MatchOut(match_id=2)
        assert match.match_id == 2
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 16, f"expected 50 fig cards between 3 players (16), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"
    finally:
        reset()

def test_match_4_players():
    reset()
    generate_test_room()
    has_turn_count = 0
    try:
        match = MatchOut(match_id=3)
        assert match.match_id == 3
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 12, f"expected 50 fig cards between 4 players (12), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"
    finally:
        reset()

def test_match_a_player():
    reset()
    generate_test_room()
    try:
        match = MatchOut(match_id=6)
        assert False
    except ValueError as e:
        assert True
    finally:
        reset()

def test_match_5_players():
    reset()
    generate_test_room()
    try:
        match = MatchOut(match_id=5)
        assert False
    except ValueError as e:
        assert True
    finally:
        reset()

def test_match_without_room():
    try:
        match = MatchOut(match_id=8)
        assert False
    except ValueError as e:
        assert True

def test_dup_match():
    try:
        MatchOut(match_id=1) # theese already added in MATCHS
        MatchOut(match_id=2)
        MatchOut(match_id=3)
        assert False
    except ValueError as e:
        assert True


def test_no_full_room():
    reset()
    generate_test_room()
    try:
        match = MatchOut(match_id=4)
        assert False
    except ValueError as e:
        assert True