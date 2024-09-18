from typing import List
from pydantic import BaseModel
from board import Board
from fig_card import FigCard, CardColor, FigType
from mov_card import MovCard, MovType
from player import Player
import random

class Match(BaseModel):
    match_id: int
    players_names: List[str]
    board: Board
    players: List[Player]

    def __init__(self, match_id: int, players_names: List[str]):
        board = self.create_board(match_id)
        players = self.create_players(match_id, players_names)
        super().__init__(match_id=match_id, players_names=players_names, board=board, players=players)
        self.validate_match()

    def validate_match(self):
        if not len(self.players_names) in range(2, 5):
            raise ValueError("There are not between 2 and 4 players")   
        if len(self.players_names) != len(set(self.players_names)):
            raise ValueError("Player names must be unique")     
        turns_count = sum(player.has_turn for player in self.players)
        if turns_count != 1:
            raise ValueError("There must be exactly one player with the turn")      

    def create_board(self, match_id: int) -> Board:
        return Board(match_id)

    def create_players(self, match_id: int, players_names: List[str]) -> List[Player]:
        players = []
        index = 0
        for player_name in players_names:
            fig_cards = self.create_fig_cards(len_players=len(players_names), match_id=match_id, player_name=player_name)
            mov_cards = self.create_mov_cards(match_id=match_id, player_name=player_name)
            has_turn = index == 0
            player = Player(match_id=match_id, player_name=player_name, mov_cards=mov_cards, fig_cards=fig_cards, has_turn=has_turn)
            players.append(player)
            index = index + 1
        return players

    @staticmethod
    def create_fig_cards(len_players: int, match_id: int, player_name: str) -> List[FigCard]:
        fig_cards = []
        white_figs = list(FigType)[:7]
        for i in range(50 // len_players):
            new_fig_card = FigCard(match_id=match_id, player_name=player_name, card_color=CardColor.WHITE, fig_type=random.choice(white_figs))
            fig_cards.append(new_fig_card)
        return fig_cards

    @staticmethod
    def create_mov_cards(match_id: int, player_name: str) -> List[MovCard]:
        mov_cards = []
        for i in range(3):
            new_mov_card = MovCard(match_id=match_id, player_name=player_name, mov_type=random.choice(list(MovType)))
            mov_cards.append(new_mov_card)
        return mov_cards
