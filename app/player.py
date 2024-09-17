from typing import List
from mov_card import MovCard, MovType
from fig_card import FigCard, FigType, CardColor
import random

class Player():

    def __init__(self,game_id,player_name,mov_cards,fig_cards):
        self.game_id: int = game_id
        self.player_name: str = player_name
        self.mov_cards: List[MovCard] = mov_cards
        self.fig_cards: List[FigCard] = fig_cards # 25 if game init with 2 players, 16 if init with 3 and 12 if init with 4   
        self.validate()

    def validate(self):
        if not (0 <= len(self.mov_cards) <= 3):
            raise ValueError('mov_cards list must contain between 0 and 3 items')
        if not (0 <= len(self.fig_cards) <= 25):
            raise ValueError('fig_cards list must contain between 0 and 25 items')

    def print_player(self):
        print(f"game id: {self.game_id}\n") 
        print(f"player name: {self.player_name}\n")
        print("mov cards:\n")
        for mov_card in self.mov_cards:
            mov_card.print_mov_card()
        print("fig cards:\n")
        for fig_card in self.fig_cards:
            fig_card.print_fig_card()