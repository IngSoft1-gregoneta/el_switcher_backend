from fastapi.testclient import TestClient
import switcher
from main import app
from uuid import uuid4
import json
from models.room import *
from main import app, chat_manager, manager
from uuid import uuid4
from state_handler import *
from figure_detector import figures_detector

client = TestClient(app)
repo = RoomRepository()

from models.match import *
from models.room import * 

repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd = Room(
                room_name="Room 1",
                room_id=str(room_id),
                players_expected=4,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo","Yamil","Facu"]),
                is_active=True
            )
        db.add(roombd)
        db.commit()
    finally:
        db.close()    

def generate_test_match():
    try:
        match = MatchOut(match_id=room_id)
        repo_match.create_match(match)
    except:
        assert False, f"Creando mal match en db"

def test_chat_connection_and_message():
    reset()
    generate_test_room()
    generate_test_match()
    user_id = uuid4()
    with client.websocket_connect(f"/websocket/chat/{user_id}") as websocket:
        test_message = "Hola, este es un mensaje de prueba"
        websocket.send_text(test_message)

        response = websocket.receive_text()
        data = json.loads(response)
        
        assert data["user_id"] == str(user_id)
        assert data["content"] == test_message

def test_websocket_chat_user_disconnect():
    reset()
    generate_test_room()
    generate_test_match()
    user_id = uuid4()
    with client.websocket_connect(f"/websocket/chat/{user_id}") as websocket:
        websocket.close()
    
    assert user_id not in chat_manager.active_connections

def test_websocket_chat_broadcast_message():
    reset()
    generate_test_room()
    generate_test_match()
    user_id_1 = uuid4()
    user_id_2 = uuid4()
    
    with client.websocket_connect(f"/websocket/chat/{user_id_1}") as ws1, \
               client.websocket_connect(f"/websocket/chat/{user_id_2}") as ws2:
        
        test_message = "Mensaje de usuario 1"
        ws1.send_text(test_message)
        
        response_1 = ws1.receive_text()
        response_2 = ws2.receive_text()
        
        data_1 = json.loads(response_1)
        data_2 = json.loads(response_2)
        
        assert data_1["content"] == test_message
        assert data_2["content"] == test_message
        assert data_1["user_id"] == str(user_id_1)
        assert data_2["user_id"] == str(user_id_1)

def test_leave_match_sends_leave_message():
    reset()
    generate_test_room()
    generate_test_match()
    user_id = uuid4()
    player_name = "Braian"
    with client.websocket_connect(f"/websocket/chat/{user_id}") as websocket:

        response = client.put(f"/matchs/leave_match/{room_id}/{player_name}/{user_id}")
        
        assert response.status_code == 202

        websocket_response = websocket.receive_text()
        data = json.loads(websocket_response)
        
        assert data["event_type"] == "leave_match"
        assert data["content"] == f"El jugador {player_name} abandonó la partida"

def test_sends_parcial_move_message():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    add_parcial_match(match)
    user_id = uuid4()
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

        with client.websocket_connect(f"/websocket/chat/{user_id}") as ws1, \
               client.websocket_connect(f"/ws/{user_id}") as ws2:
            
            manager.bind_room(room_id, user_id)
            
            response = client.put(f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}")
            
            assert response.status_code == status.HTTP_200_OK
            websocket_response = ws1.receive_text()
            data = json.loads(websocket_response)
            assert data["event_type"] == "parcial_move"
            assert data["content"] == f"El jugador {player.player_name} realizó un movimiento"


def test_sends_revert_move_message():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    add_parcial_match(match)
    user_id = uuid4()
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

        with client.websocket_connect(f"/websocket/chat/{user_id}") as ws1, \
               client.websocket_connect(f"/ws/{user_id}") as ws2:
            
            manager.bind_room(room_id, user_id)
            
            response = client.put(f"/parcial_move/{room_id}/{player.player_name}/{card_index}/{x1}/{y1}/{x2}/{y2}")
            
            assert response.status_code == status.HTTP_200_OK
        
        revert_response = client.put(f"/revert_movement/{room_id}/{player.player_name}")
    
        assert revert_response.status_code == status.HTTP_200_OK
        websocket_response = ws1.receive_text()
        data = json.loads(websocket_response)
        assert data["event_type"] == "revert_move"
        assert data["content"] == f"El jugador {player.player_name} revirtió un movimiento"


def test_sends_discard_fig_message():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    add_parcial_match(match)
    user_id = uuid4()
    match = get_parcial_match(room_id)

    for tile in match.board.tiles:
        tile.tile_color = TileColor.RED.value
    match.board.tiles[0].tile_color = TileColor.BLUE.value
    match.board.tiles[1].tile_color = TileColor.BLUE.value
    match.board.tiles[2].tile_color = TileColor.BLUE.value
    match.board.tiles[3].tile_color = TileColor.BLUE.value
    match.board = figures_detector(match.board, [FigType.fige06.value])
    player = match.get_player_by_name(match.players[0].player_name)
    player.fig_cards[0].fig_type = FigType.fige06.value
    card_index = 0
    x = 0
    y = 0

    with client.websocket_connect(f"/websocket/chat/{user_id}") as ws1, \
               client.websocket_connect(f"/ws/{user_id}") as ws2:
        
        manager.bind_room(room_id, user_id)
        response = client.put(f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}")
        assert response.status_code == status.HTTP_200_OK


        websocket_response = ws1.receive_text()
        data = json.loads(websocket_response)
        assert data["event_type"] == "discard_fig"
        assert data["content"] == f"El jugador {player.player_name} descartó una figura"


def test_sends_block_fig_message():
    reset()
    generate_test_room()
    generate_test_match()
    match = repo_match.get_match_by_id(room_id)
    add_parcial_match(match)
    user_id = uuid4()
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
    other_player = match.get_player_by_name(match.players[1].player_name)
    other_player.fig_cards[0].fig_type = FigType.fige06.value
    card_index = 0
    x = 0
    y = 0

    with client.websocket_connect(f"/websocket/chat/{user_id}") as ws1, \
               client.websocket_connect(f"/ws/{user_id}") as ws2:
        
        manager.bind_room(room_id, user_id)
        response = client.put(f"/block_figure/{room_id}/{player.player_name}/{other_player.player_name}/{card_index}/{x}/{y}")
        assert response.status_code == status.HTTP_200_OK


        websocket_response = ws1.receive_text()
        data = json.loads(websocket_response)
        assert data["event_type"] == "block_fig"
        assert data["content"] == f"El jugador {player.player_name} bloqueó una figura"

reset()