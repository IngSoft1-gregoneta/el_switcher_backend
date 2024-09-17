from mov_card import MovCard, MovType
import random

def test_valid_mov_card():
    try:
        card = MovCard(game_id=1, player_name="Player1", mov_type=random.choice(list(MovType)))
        card.print_mov_card()
    except ValueError as e:
        print(f"Error: {e}")
        assert False

def test_bad_mov():
    try:
        MovCard(game_id=1, player_name="Player1", mov_type="Side")
        assert False
    except ValueError as e:
        print(f"Error: {e}")