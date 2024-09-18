from player import Player
from mov_card import MovCard, MovType
from fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[:7]
blue_figs = list(FigType)[7:]

def test_valid_player():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            mov_cards.append(MovCard(match_id=1, player_name="Player1", mov_type=random.choice(list(MovType))))
        for i in range(25):
            fig_cards.append(FigCard(match_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(white_figs)))
        Player(
           match_id=1,
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        
    except ValueError as e:
        print(f"Error: {e}")
        assert False

def test_invalid_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(4):
            mov_cards.append(MovCard(match_id=1, player_name="Player1", mov_type=random.choice(list(MovType))))
        for i in range(25):
            fig_cards.append(FigCard(match_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(white_figs)))
        Player(
            match_id=1,
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )

        assert False
        
    except ValueError as e:
        print(f"Error: {e}")

def test_invalid_fig_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            mov_cards.append(MovCard(match_id=1, player_name="Player1", mov_type=random.choice(list(MovType))))
        for i in range(26):
            fig_cards.append(FigCard(match_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=random.choice(white_figs)))
        Player(
            match_id=1,
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )
        assert False
        
    except ValueError as e:
        print(f"Error: {e}")
