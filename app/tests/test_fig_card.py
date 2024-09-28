from models.fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[:7]
blue_figs = list(FigType)[7:]

def test_valid_fig_card():
    try:
        FigCard(match_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=True)
        FigCard(match_id=1, player_name="Player1", card_color=CardColor.BLUE, fig_type=random.choice(blue_figs), is_visible=False)
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_fig_card_str():
    try:
        FigCard(match_id=1, player_name="Player1", card_color="White", fig_type="L", is_visible=False)
        FigCard(match_id=1, player_name="Player1", card_color="Blue", fig_type="B1", is_visible=False)
    except ValueError as e:
        assert False, f"Error: {e}"

def test_bad_color_fig_card():
    try:
        FigCard(match_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(blue_figs), is_visible=False)
        FigCard(match_id=1, player_name="Player1", card_color=CardColor.BLUE, fig_type=random.choice(white_figs), is_visible=False)
        assert False
    except ValueError as e:
        assert True

def test_invalid_color():
    try:
        FigCard(match_id=1, player_name="Player1", card_color="Red", fig_type=random.choice(blue_figs), is_visible=False)
        FigCard(match_id=1, player_name="Player1", card_color="Green", fig_type=random.choice(white_figs), is_visible=False)
        assert False
    except ValueError as e:
        assert True
