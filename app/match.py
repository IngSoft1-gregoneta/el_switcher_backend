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

    def validate_room(self, match_id: int) -> List[str]:
        rooms_whit_match_id = 0   
        for room in ROOMS:
            if room["room_id"] == match_id:
                 room_of_match = room
                 rooms_whit_match_id = rooms_whit_match_id + 1
        if rooms_whit_match_id != 1:
            raise ValueError("There must be exactly one room per match")  
        for match in MATCHS:
            if match["match_id"] == match_id:
                raise ValueError("Can not be more than a match with same id")  
        if not len(room_of_match["players_names"]) in range(2, 5):
            raise ValueError("There are not between 2 and 4 players") 
        if room_of_match["players_expected"] != len(room_of_match["players_names"]):
            raise ValueError("There must be exactly players expected amount of players")  
        return room_of_match["players_names"]
 
    def validate_match(self):
        turns_count = sum(player.has_turn for player in self.players)
        if turns_count != 1:
            raise ValueError("There must be exactly one player with the turn")      

    def create_board(self, match_id: int) -> Board:
        return Board(match_id)

    def create_players(self, match_id: int) -> List[Player]:
        players_names = self.validate_room(match_id)
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

def get_match_by_id(input: id):
    for match in MATCHS:
        if match["match_id"] == input:
            return match
    raise ValueError("There is no match with id: {input}")

def check_turn(match: Match) -> Player:
    for player in match.players:
        if player.has_turn == True:
            return player
    raise ValueError("No player has the turn")

def next_turn(match: Match):
    done = False
    for i, player in match.players:
        if player.has_turn:
            player.has_turn = False
            next_player_index: int = (i + 1) % len(match.players)
            match.players[next_player_index].has_turn = True
            done = True
            break
    if not done:
        raise ValueError("An error occured when trying to pass to the next turn")