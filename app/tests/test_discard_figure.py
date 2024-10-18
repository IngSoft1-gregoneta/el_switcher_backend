from fastapi.testclient import TestClient
from figure_detector import figures_detector
from models.room import *
from state_handler import *
from main import app, manager
repo = RoomRepository()

from models.match import *
from models.room import * 
from models.visible_match import *
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
        assert False, f"Creando mal matchs en db"

def test_discard_fig():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    user_id = uuid1()
    match = get_parcial_match(room_id)
    for tile in match.board.tiles:
        tile.tile_color = TileColor.RED.value
    match.board.tiles[0].tile_color = TileColor.BLUE.value
    match.board.tiles[1].tile_color = TileColor.BLUE.value
    match.board.tiles[2].tile_color = TileColor.BLUE.value
    match.board.tiles[3].tile_color = TileColor.BLUE.value
    match.board = figures_detector(match.board, [FigType.fige06.value])
    init_board = match.board
    player = match.get_player_by_name(match.players[0].player_name)
    player.fig_cards[0].fig_type = FigType.fige06.value
    card_index = 0
    x = 0
    y = 0
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room_id, user_id)
        response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == None
        # check db update
        after_discard_db_match = repo_match.get_match_by_id(room_id)
        assert len(after_discard_db_match.players[0].fig_cards) == 24 
        visible_fig_cards_count = 0
        for card in after_discard_db_match.players[0].fig_cards:
            if card.is_visible: 
                visible_fig_cards_count += 1
        assert visible_fig_cards_count == 2
        # check reinit parcial states
        after_discard_match = get_parcial_match(room_id)
        assert after_discard_match.state == 0
        visible_match = VisibleMatchData(room_id, player.player_name)
        assert visible_match.me.deck_len == 24
        assert len(visible_match.me.visible_fig_cards) == 2 
        # these changes should be not confirmed
        after_discard_match.board = Board()
        # check player got a new fig card of his deck
        response = client.put(f"/matchs/end_turn/{room_id}/{player.player_name}")
        assert response.status_code == status.HTTP_200_OK
        after_end_turn_match = get_parcial_match(room_id)
        assert after_end_turn_match.state == 0
        visible_fig_cards_count = 0
        for card in after_end_turn_match.players[0].fig_cards:
            if card.is_visible: 
                visible_fig_cards_count += 1
        assert visible_fig_cards_count == 3
        assert len(after_end_turn_match.players[0].fig_cards) == 24
        # check tiles after discard fig are the same color
        for i in range(36):
            assert init_board.tiles[i].tile_color == after_end_turn_match.board.tiles[i].tile_color

def test_match_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    x = 0
    y = 0
    response = client.put(f"/discard_figure/{room_id2}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Match not found'}

def test_player_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    card_index = 0
    x = 0
    y = 0
    no_player_name = 'Grego'
    response = client.put(f"/discard_figure/{room_id}/{no_player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Player not found'}

def test_player_no_turn():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[1].player_name)
    card_index = 0
    x = 0
    y = 0
    response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail' : 'Player has not turn'}

def test_card_not_found():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 25
    x = 0
    y = 0
    response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Card not found'}

def test_card_not_visible():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 3
    x = 0
    y = 0
    response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail' : 'Card is not visible'}

def test_fig_no_match():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    for tile in match.board.tiles:
        tile.tile_color = TileColor.RED.value
    match.board.tiles[0].tile_color = TileColor.BLUE.value
    match.board.tiles[1].tile_color = TileColor.BLUE.value
    match.board.tiles[2].tile_color = TileColor.BLUE.value
    match.board.tiles[3].tile_color = TileColor.BLUE.value
    match.board = figures_detector(match.board, [FigType.fige06.value])
    player = match.get_player_by_name(match.players[0].player_name)
    player.fig_cards[0].fig_type = FigType.fig06.value
    card_index = 0
    x = 0
    y = 0
    response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail' : 'Fig card not match with figure'}

def test_invalid_positions():
    reset()
    generate_test_room()
    generate_test_match()
    match1 = repo_match.get_match_by_id(room_id)
    add_parcial_match(match1)
    
    match = get_parcial_match(room_id)
    player = match.get_player_by_name(match.players[0].player_name)
    card_index = 0
    x = 6
    y = 6
    response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail' : 'Invalid positions'}