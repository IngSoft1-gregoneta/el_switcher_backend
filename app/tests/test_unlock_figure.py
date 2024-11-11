from fastapi.testclient import TestClient
from figure_detector import figures_detector
from main import app, manager
from models.match import *
from models.room import *
from models.visible_match import *
from state_handler import *

client = TestClient(app)
repo_room = RoomRepository()
repo_match = MatchRepository()

room_id = uuid1()
not_room_id = uuid1()


def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()


def generate_test_room():
    db = Session()
    try:
        roombd = Room(
            room_name="Room 1",
            room_id=str(room_id),
            players_expected=2,
            owner_name="Braian",
            private=False,
            password=None,
            players_names=json.dumps(["Braian", "Tadeo"]),
            is_active=True,
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
    player.fig_cards[1].is_blocked = True
    player.fig_cards.remove(player.fig_cards[2])
    card_index = 0
    x = 0
    y = 0
    with client.websocket_connect(f"/ws/{user_id}"):
        manager.bind_room(room_id, user_id)
        response = client.put(
            f"/discard_figure/{room_id}/{player.player_name}/{card_index}/{x}/{y}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == None
        # check db update
        after_discard_db_match = repo_match.get_match_by_id(room_id)
        db_player = after_discard_db_match.players[0]
        assert db_player.fig_cards[0].is_visible == True
        assert len(db_player.fig_cards) == 23
        visible_fig_cards_count = 0
        for card in db_player.fig_cards:
            if card.is_visible:
                visible_fig_cards_count += 1
        assert visible_fig_cards_count == 1
        # check reinit parcial states
        after_discard_match = get_parcial_match(room_id)
        assert after_discard_match.state == 0
        visible_match = VisibleMatchData(room_id, player.player_name)
        assert visible_match.me.deck_len == 23
        assert len(visible_match.me.visible_fig_cards) == 1
        # these changes should be not confirmed
        after_discard_match.board = Board()
        # check player got a new fig card of his deck
        response = client.put(f"/matchs/end_turn/{room_id}/{player.player_name}")
        assert response.status_code == status.HTTP_200_OK
        after_end_turn_match = get_parcial_match(room_id)
        player = after_end_turn_match.players[0]
        assert after_end_turn_match.state == 0
        visible_fig_cards_count = 0
        for card in player.fig_cards:
            if card.is_visible:
                visible_fig_cards_count += 1
        assert visible_fig_cards_count == 3
        assert len(player.fig_cards) == 23
        # check tiles after discard fig are the same color
        for i in range(36):
            assert (
                init_board.tiles[i].tile_color
                == after_end_turn_match.board.tiles[i].tile_color
            )
        reset()

