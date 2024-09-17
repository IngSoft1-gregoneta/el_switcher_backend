from fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[:7]
blue_figs = list(FigType)[7:]

def test_valid_fig_card():
    try:
        card1 = FigCard(game_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(white_figs))
        card2 = FigCard(game_id=1, player_name="Player1", card_color=CardColor.BLUE, fig_type=random.choice(blue_figs))
        card1.print_fig_card()
        card2.print_fig_card()
    except ValueError as e:
        print(f"Error: {e}")
        assert False

def test_invalid_white_card():
    try:
        FigCard(game_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(blue_figs))
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_invalid_blue_card():
    try:
        FigCard(game_id=1, player_name="Player1", card_color=CardColor.BLUE, fig_type=random.choice(white_figs))
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_bad_fig_type():
    try:
        FigCard(game_id=1, player_name="Player1", card_color=random.choice(list(CardColor)), fig_type='L')
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_bad_card_color():
    try:
        FigCard(game_id=1, player_name="Player1", card_color='White', fig_type=random.choice(white_figs))
        assert False
    except ValueError as e:
        print(f"Error: {e}")