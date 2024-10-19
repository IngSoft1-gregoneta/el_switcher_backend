from models.player import Player
from models.mov_card import MovCard, MovType
from models.fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[1:8]
blue_figs = list(FigType)[8:]

def test_valid_player():
    try:
        mov_cards = []
        fig_cards = []
        for _ in range(3):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for _ in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        
    except ValueError:
        assert True


def test_invalid_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for _ in range(4):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for _ in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )

        assert False
        
    except ValueError:
        assert True


def test_invalid_fig_cards():
    try:
        mov_cards = []
        fig_cards = []
        for _ in range(3):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for _ in range(26):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )
        assert False
        
    except ValueError:
        assert True
