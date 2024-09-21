from models.mov_card import MovCard, MovType
import random

def test_random_mov_card():
    match_id = 1
    player_name = "Player1"
    try:
        card = MovCard(match_id=match_id, player_name=player_name)
        assert card.match_id == match_id, f"game id {card.match_id} must be {match_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type in list(MovType), f"{card.mov_type} is not a valid mov card"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card():
    match_id = 1
    player_name = "Player1"
    mov_type = MovType.SIDE
    try:
        card = MovCard(match_id=match_id, player_name=player_name, mov_type=mov_type)
        assert card.match_id == match_id, f"game id {card.match_id} must be {match_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type == mov_type, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card_str():
    match_id = 1
    player_name = "Player1"
    mov_type = "Side"
    try:
        card = MovCard(match_id=match_id, player_name=player_name, mov_type=mov_type)
        assert card.match_id == match_id, f"game id {card.match_id} must be {match_id}"
        assert card.player_name == player_name, f"player name {card.player_name} must be {player_name}"
        assert card.mov_type == MovType.SIDE, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"
    
def test_invalid_mov_card_str():
    match_id = 1
    player_name = "Player1"
    mov_type = "Diagonal"
    try:
        card = MovCard(match_id=match_id, player_name=player_name, mov_type=mov_type)
        assert False, f"{card.mov_type} is not a mov type"
    except ValueError as e:
        assert True