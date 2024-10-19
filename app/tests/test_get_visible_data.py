from fastapi.testclient import TestClient
from fastapi import status
from models.room import *
from models.visible_match import *
from main import app


client = TestClient(app)
repo = RoomRepository()

from models.match import *
from models.room import * 
from state_handler import *

repo_room = RoomRepository()
repo_match = MatchRepository()

room1_id = uuid1()
room2_id = uuid1()
room3_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()


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
        db.add(roombd1)
        db.add(roombd2)
        db.add(roombd3)
        db.commit()
    finally:
        db.close()


def generate_test_match():
    try:
        match_1 = MatchOut(match_id=room1_id)
        match_2 = MatchOut(match_id=room2_id)
        match_3 = MatchOut(match_id=room3_id)
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
        repo_match.create_match(match_3)
    except:
        assert False, f"Error al crear partidas en BD"


def verify_test_ok(match_id: UUID, player_name: str):
    match = repo_match.get_match_by_id(match_id)
    add_parcial_match(match)
    expected_response = VisibleMatchData(match_id,player_name)
    response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response.model_dump(mode="json")
    assert expected_response.match_id == str(match_id)
    has_turn_count = 0
    for player in match.players:
        if player.has_turn: has_turn_count = has_turn_count + 1
        for other_player in expected_response.other_players:
            for fig_card in player.fig_cards:
                if other_player.player_name == player.player_name:
                    if fig_card.is_visible is True:
                        assert fig_card in other_player.visible_fig_cards
                    else:
                        assert fig_card not in other_player.visible_fig_cards
            assert other_player.deck_len == len(player.fig_cards)
        if expected_response.me.player_name == player.player_name:
            for fig_card in player.fig_cards:
                if fig_card.is_visible is True:
                    assert fig_card in expected_response.me.visible_fig_cards
                else:
                    assert fig_card not in expected_response.me.visible_fig_cards
            assert expected_response.me.deck_len == len(player.fig_cards)
            for mov_card in player.mov_cards:
                assert mov_card in expected_response.me.mov_cards
    assert has_turn_count == 1
    assert expected_response.board == match.board

def test_get_visible_data_in_match_of_2_players():
    reset()
    generate_test_room()
    generate_test_match()
    match_id = room1_id
    player_name = "Braian"
    verify_test_ok(match_id=match_id, player_name=player_name)
    reset()

def test_get_visible_data_in_match_of_3_players():
    generate_test_room()
    generate_test_match()
    match_id = room2_id
    player_name = "Tadeo"
    verify_test_ok(match_id=match_id, player_name=player_name)
    reset()

def test_get_visible_data_in_match_of_4_players():
    generate_test_room()
    generate_test_match()
    match_id = room3_id
    player_name = "Yamil"
    verify_test_ok(match_id=match_id, player_name=player_name)
    reset()

def test_get_visible_data_in_no_match():
    generate_test_room()
    generate_test_match()
    match_id = uuid1()
    player_name = "Yamil"
    response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Partida no encontrada'}
    try:
        VisibleMatchData(match_id=match_id,player_name=player_name)
    except:
        assert True
    reset()

def test_get_visible_data_of_match_by_no_player():
    generate_test_room()
    generate_test_match()
    match_id = room1_id
    player_name = "Yamil"
    response = client.get(f"/matchs/visible_match/{match_id}/{player_name}")    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': f'Jugador {player_name} No encontrado'}
    try:
        VisibleMatchData(match_id=match_id,player_name=player_name)
    except:
        assert True
    reset()