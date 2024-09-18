from mov_card import MovCard, MovType
import random

def test_random_mov_card():
    game_id = 1
    player_name = "Player1"
    try:
        card = MovCard(game_id=game_id, player_name=player_name)
        assert card.game_id == game_id, f"game id {card.game_id} must be {game_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type in list(MovType), f"{card.mov_type} is not a valid mov card"
    except ValueError as e:
        print(f"Error: {e}")

def test_valid_mov_card():
    game_id = 1
    player_name = "Player1"
    mov_type = MovType.SIDE
    try:
        card = MovCard(game_id=game_id, player_name=player_name, mov_type=mov_type)
        assert card.game_id == game_id, f"game id {card.game_id} must be {game_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type == mov_type, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        print(f"Error: {e}")

def test_valid_mov_card_str():
    game_id = 1
    player_name = "Player1"
    mov_type = "Side"
    try:
        card = MovCard(game_id=game_id, player_name=player_name, mov_type=mov_type)
        assert card.game_id == game_id, f"game id {card.game_id} must be {game_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type == MovType.SIDE, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        print(f"Error: {e}")
    
def test_invalid_mov_card_str():
    game_id = 1
    player_name = "Player1"
    mov_type = "Diagonal"
    try:
        card = MovCard(game_id=game_id, player_name=player_name, mov_type=mov_type)
        assert False, f"{card.mov_type} is not a mov type"
    except ValueError as e:
        print(f"Error: {e}")