from models.player import Player
from models.mov_card import MovCard, MovType, MovStatus
from models.fig_card import FigCard, CardColor, FigType
import random

white_figs = list(FigType)[:7]
blue_figs = list(FigType)[7:]

def test_valid_player():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for i in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        
    except ValueError as e:
        assert True


def test_invalid_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(4):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for i in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )

        assert False
        
    except ValueError as e:
        assert True


def test_invalid_fig_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType))))
        for i in range(26):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        Player(
            player_name="Player1",
            mov_cards=mov_cards,
            fig_cards=fig_cards,
            has_turn=True
        )
        assert False
        
    except ValueError as e:
        assert True
<<<<<<< HEAD
=======

def test_dont_show_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            mov_cards.append(MovCard(mov_type=random.choice(list(MovType)), mov_status=MovStatus.HELD))
        for i in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        player = Player(
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        assert [] == player.show_mov_card(), "No movement cards should be shown if all are held."

    except ValueError as e:
        assert False, f"Error: {e}"

def test_show_played_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            card = (MovCard(mov_type=random.choice(list(MovType)), mov_status=MovStatus.PLAYED))
            card.is_used = True
            mov_cards.append(card)
        for i in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        player = Player(
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        assert mov_cards == player.show_mov_card(), "Show the movement cards that are played"

    except ValueError as e:
        assert False, f"Error: {e}"

def test_show_confirmed_mov_cards():
    try:
        mov_cards = []
        fig_cards = []
        for i in range(3):
            card = (MovCard(mov_type=random.choice(list(MovType)), mov_status=MovStatus.CONFIRMED))
            card.is_used = True
            mov_cards.append(card)
        for i in range(25):
            fig_cards.append(FigCard(card_color=CardColor.WHITE, fig_type=random.choice(white_figs), is_visible=False))
        player = Player(
           player_name="Player1",
           mov_cards=mov_cards,
           fig_cards=fig_cards,
           has_turn=True
        )
        assert mov_cards == player.show_mov_card(), "Show the movement cards that are confirmed"

    except ValueError as e:
        assert False, f"Error: {e}"





>>>>>>> 79d6e0cfd1b3846714fb454e68f3731c17cb46fd
