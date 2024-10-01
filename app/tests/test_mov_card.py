from models.mov_card import MovCard, MovType
import random

def test_random_mov_card():
    try:
        card = MovCard()
        assert card.mov_type in list(MovType), f"{card.mov_type} is not a valid mov card"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card():
    mov_type = random.choice(list(MovType))
    try:
        card = MovCard(mov_type=mov_type)
        assert card.mov_type == mov_type, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_mov_card_str():
    mov_type = "mov1"
    try:
        card = MovCard(mov_type=mov_type)
        assert card.mov_type == MovType.mov1, f"mov type {card.mov_type} must be {mov_type}"
    except ValueError as e:
        assert False, f"Error: {e}"
    
def test_invalid_mov_card_str():
    mov_type = "Diagonal"
    try:
        card = MovCard(mov_type=mov_type)
        assert False, f"{card.mov_type} is not a mov type"
    except ValueError as e:
        assert True