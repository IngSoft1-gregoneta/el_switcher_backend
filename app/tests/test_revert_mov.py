from fastapi.testclient import TestClient
from models.room import *
from state_handler import *
from main import app, manager
repo = RoomRepository()

from models.match import *
from models.room import * 
import switcher 

client = TestClient(app)

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()
room_id2 = uuid1()
def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()
    empty_parcial_states(room_id)
    empty_parcial_states(room_id2)

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=str(room_id),
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        roombd2 = Room(
                room_name="Room 2",
                room_id=str(room_id2),
                players_expected=2,
                owner_name="Yamil",
                players_names=json.dumps(["Yamil","Tadeo"]),
                is_active=True
            )
        db.add(roombd1)
        db.add(roombd2)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match_1 = MatchOut(
                match_id=room_id
            )
        match_2 = MatchOut(
            match_id=room_id2
        )
        repo_match.create_match(match_1)
        repo_match.create_match(match_2)
    except:
        assert False, f"Error al crear partidas en BD"

def test_revert_mov():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    user_id = uuid1()
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    card = player.mov_cards[card_index]
    
    x1 = 3
    y1 = 3
    x2 = x1 + card.vectors[0][0]
    y2 = y1 + card.vectors[0][1]
    
    while not switcher.is_valid_movement(card.mov_type, x1, y1, x2, y2):
        x1 = random.randrange(0, 5)
        y1 = random.randrange(0, 5)
        x2 = x1 + card.vectors[0][0]
        y2 = y1 + card.vectors[0][1]
    
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room_id, user_id)
        response = client.put(f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}")
        match = get_parcial_match(room_id)
        assert response.status_code == status.HTTP_200_OK
        assert match.state == 1
    
    revert_response = client.put(f"/revert_movement/{room_id}/{player.player_name}")
    reverted_match = get_parcial_match(room_id)
    
    assert revert_response.status_code == status.HTTP_200_OK
    assert reverted_match.state == 0
    assert not card.is_used 


def test_revert_without_previous_move():
    reset()
    generate_test_room()
    generate_test_match()
    match2 = repo_match.get_match_by_id(room_id2)
    add_parcial_match(match2)

    match = get_parcial_match(room_id2)
    player = match.get_player_by_name(match.players[0].player_name)

    revert_response = client.put(f"/revert_movement/{room_id2}/{player.player_name}")

    assert revert_response.status_code == 400
    assert revert_response.json() == {'detail': 'No se puede retroceder mas del estado inicial'}


def test_revert_not_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    user_id = uuid1()
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    player_without_turn = "Tadeo"
    card = player.mov_cards[card_index]
    
    x1 = 3
    y1 = 3
    x2 = x1 + card.vectors[0][0]
    y2 = y1 + card.vectors[0][1]
    
    while not switcher.is_valid_movement(card.mov_type, x1, y1, x2, y2):
        x1 = random.randrange(0, 5)
        y1 = random.randrange(0, 5)
        x2 = x1 + card.vectors[0][0]
        y2 = y1 + card.vectors[0][1]
    
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room_id, user_id)
        response = client.put(f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}")
        match = get_parcial_match(room_id)
        assert response.status_code == status.HTTP_200_OK
        assert match.state == 1
    
    revert_response = client.put(f"/revert_movement/{room_id}/{player_without_turn}")
    assert revert_response.status_code == 400
    assert revert_response.json() == {'detail': 'El jugador no tiene el turno'}


reset()