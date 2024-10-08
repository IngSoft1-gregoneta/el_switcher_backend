from typing import List
from pydantic import BaseModel
from .mov_card import MovCard
from .fig_card import FigCard

class Player(BaseModel):
    player_name: str
    mov_cards: List[MovCard]
    fig_cards: List[FigCard]
    has_turn: bool

    def __init__(self, player_name: str, mov_cards: List[MovCard], fig_cards: List[FigCard], has_turn: bool):
        super().__init__(player_name=player_name, mov_cards=mov_cards, fig_cards=fig_cards, has_turn=has_turn)
        self.validate()

    def validate(self):
        if not (0 <= len(self.mov_cards) <= 3):
            raise ValueError('mov_cards list must contain between 0 and 3 items')
        if not (0 <= len(self.fig_cards) <= 25):
            raise ValueError('fig_cards list must contain between 0 and 25 items')
        
    def show_mov_card(self):
        if self.has_turn == True:
         used_mov_cards = [card for card in self.mov_cards if card.is_used]
         return used_mov_cards
        else:
            raise ValueError("The player has not the turn")
