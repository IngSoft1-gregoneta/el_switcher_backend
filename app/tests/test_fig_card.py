from models.fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[1:8]
blue_figs = list(FigType)[8:]

def test_valid_fig_card():
    try:
        FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=True, is_blocked=False)
        FigCard(card_color=CardColor.BLUE, fig_type=random.choice(blue_figs), is_visible=False, is_blocked=False)
    except ValueError as e:
        assert False, f"Error: {e}"

def test_valid_fig_card_str():
    try:
        FigCard(card_color="White", fig_type="fige01", is_visible=False, is_blocked=False)
        FigCard(card_color="Blue", fig_type="fig01", is_visible=False, is_blocked=False)
    except ValueError as e:
        assert False, f"Error: {e}"

def test_bad_color_fig_card():
    try:
        FigCard(card_color=CardColor.WHITE, fig_type=random.choice(blue_figs), is_visible=False, is_blocked=False)
        FigCard(card_color=CardColor.BLUE, fig_type=random.choice(white_figs), is_visible=False, is_blocked=False)
        assert False
    except ValueError as e:
        assert True

def test_invalid_color():
    try:
        FigCard(card_color="Red", fig_type=random.choice(blue_figs), is_visible=False, is_blocked=False)
        FigCard(card_color="Green", fig_type=random.choice(white_figs), is_visible=False, is_blocked=False)
        assert False
    except ValueError as e:
        assert True
