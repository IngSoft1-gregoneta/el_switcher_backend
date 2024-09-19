from typing import List
from pydantic import BaseModel
from board import Board
from fig_card import FigCard, CardColor, FigType
from mov_card import MovCard, MovType
from player import Player
from room import ROOMS
import random

class MatchIn(BaseModel):
    room_id: int

class Match(BaseModel):
    match_id: int
    board: Board
    players: List[Player]

    def __init__(self, match_id: int):
        board = self.create_board(match_id)
        players = self.create_players(match_id)
        super().__init__(match_id=match_id, board=board, players=players)
        self.validate_match()

    def validate_match(self):
        rooms_whit_match_id = 0   
        for room in ROOMS:
            if room["room_id"] == self.match_id:
                 room_of_match = room
                 rooms_whit_match_id = rooms_whit_match_id + 1
        if rooms_whit_match_id != 1:
            raise ValueError("There must be exactly one room per match")  
        for match in MATCHS:
            if match["match_id"] == self.match_id:
                raise ValueError("Can not be more than a match with same id")  
        if not len(self.players) in range(2, 5):
            raise ValueError("There are not between 2 and 4 players")   
        turns_count = sum(player.has_turn for player in self.players)
        if room_of_match["players_expected"] != len(room_of_match["players_names"]):
            raise ValueError("There must be exactly players expected amount of players")      
        if turns_count != 1:
            raise ValueError("There must be exactly one player with the turn")      

    def create_board(self, match_id: int) -> Board:
        return Board(match_id)

    def create_players(self, match_id: int) -> List[Player]:
        players_names = []
        for room in ROOMS:
            if room["room_id"] == match_id:
                players_names = room["players_names"]
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

MATCHS = [
]
