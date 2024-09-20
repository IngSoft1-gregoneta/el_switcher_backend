from match import *
from room import * 


def test_match_2_players():
    room_id = 1
    room_name = "Room 1"
    players_expected = 2
    players_names = ['Yamil','Tadeo']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    has_turn_count = 0
    try:
        match = Match(match_id=room_id)
        MATCHS.append(match.model_dump())
        assert match.match_id == room_id
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 25, f"expected 50 fig cards between 2 players (25), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_3_players():
    room_id = 2
    room_name = "Room 2"
    players_expected = 3
    players_names = ['Yamil','Tadeo', 'Brian']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    has_turn_count = 0
    try:
        match = Match(match_id=room_id)
        MATCHS.append(match.model_dump())
        assert match.match_id == room_id
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 16, f"expected 50 fig cards between 3 players (16), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_4_players():
    room_id = 3
    room_name = "Room 3"
    players_expected = 4
    players_names = ['Yamil','Tadeo', 'Brian', 'Facu']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    has_turn_count = 0
    try:
        match = Match(match_id=room_id)
        MATCHS.append(match.model_dump())
        assert match.match_id == room_id
        for player in match.players:
            fig_deck_len = len(player.fig_cards)
            mov_deck_len = len(player.mov_cards)
            if player.has_turn: has_turn_count = has_turn_count + 1
            assert fig_deck_len == 12, f"expected 50 fig cards between 4 players (12), got {fig_deck_len}"
            assert mov_deck_len == 3, f"expected 3 mov fig cards, got {mov_deck_len}"
        assert has_turn_count == 1, f"more than a player can not have the turn"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_match_a_player():
    room_id = 4
    room_name = "Room 4"
    players_expected = 1
    players_names = ['Yamil']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    try:
        match = Match(match_id=room_id)
        assert False
    except ValueError as e:
        assert True

def test_match_5_players():
    room_id = 5
    room_name = "Room 1"
    players_expected = 5
    players_names = ['Yamil','Tadeo','Grego','Facu','Braian']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    try:
        match = Match(match_id=room_id)
        assert False
    except ValueError as e:
        assert True

def test_match_without_room():
    room_id = 7
    room_name = "Room 7"
    players_expected = 4
    players_names = ['Yamil','Tadeo','Grego','Facu']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    try:
        match = Match(match_id=8)
        assert False
    except ValueError as e:
        assert True

def test_dup_match():
    try:
        Match(match_id=1) # theese already added in MATCHS
        Match(match_id=2)
        Match(match_id=3)
        assert False
    except ValueError as e:
        assert True


def test_no_full_room():
    room_id = 10
    room_name = "Room 7"
    players_expected = 4
    players_names = ['Yamil','Tadeo','Grego']
    owner_name = 'Yamil'
    is_active = True
    room = RoomOut(room_id=room_id,
                   room_name=room_name,
                   players_expected=players_expected,
                   players_names=players_names,
                   owner_name=owner_name,
                   is_active=is_active)
    ROOMS.append(room.model_dump())
    try:
        match = Match(match_id=10)
        assert False
    except ValueError as e:
        assert True