from typing import List
from pydantic import BaseModel
from .board import Board
from .fig_card import FigCard, CardColor, FigType
from .mov_card import MovCard, MovType
from .player import Player
from .room import *
from repositories.room_repo import RoomRepository
import random
from typing import Tuple
    
class MatchOut(BaseModel):
    match_id: UUID
    board: Board
    players: List[Player]

    def __init__(self, match_id: UUID):
        board = self.create_board()
        players = self.create_players(match_id)
        super().__init__(match_id=match_id, board=board, players=players)
        self.validate_match()

    def validate_room(self, match_id: UUID) -> List[str]:
        repo = RoomRepository()
        rooms_whit_match_id = 0
        for room in repo.get_rooms():
            if room["room_id"] == match_id:
                 room_of_match = room
                 rooms_whit_match_id = rooms_whit_match_id + 1
        if rooms_whit_match_id != 1:
            raise ValueError("There must be exactly one room per match")  
        if not len(room_of_match["players_names"]) in range(2, 5):
            raise ValueError("There are not between 2 and 4 players") 
        if room_of_match["players_expected"] != len(room_of_match["players_names"]):
            raise ValueError("There must be exactly players expected amount of players")  
        return room_of_match["players_names"]
 
    def validate_match(self):
        turns_count = sum(player.has_turn for player in self.players)
        if turns_count != 1:
            raise ValueError("There must be exactly one player with the turn")      

    def create_board(self) -> Board:
        return Board()

    def create_players(self, match_id: UUID) -> List[Player]:
        players_names = self.validate_room(match_id)
        players = []
        
        white_deck = list(FigType)[:7] * 2  # 14 cartas blancas, dos de cada figura
        blue_deck = list(FigType)[7:] * 2  # 36 cartas azules, dos de cada figura
        random.shuffle(white_deck)
        random.shuffle(blue_deck)
        
        white_per_player = 14 // len(players_names)
        blue_per_player = 36 // len(players_names)

        index = 0
        for player_name in players_names:
            fig_cards, white_deck, blue_deck = self.create_fig_cards(white_per_player,blue_per_player,white_deck,blue_deck)
            for i in range(3): fig_cards[i].is_visible = True
            mov_cards = self.create_mov_cards()
            has_turn = index == 0
            player = Player(player_name=player_name, mov_cards=mov_cards, fig_cards=fig_cards, has_turn=has_turn)
            players.append(player)
            index = index + 1
        return players


    @staticmethod
    def create_fig_cards(white_per_player: int, 
                         blue_per_player: int, white_deck: List[FigType],
                        blue_deck: List[FigType]) -> Tuple[List[FigCard], List[FigType], List[FigType]]:
        fig_cards = []
        for i in range(white_per_player):
            fig_type = white_deck.pop(0)
            new_fig_card = FigCard(
                card_color=CardColor.WHITE,
                fig_type=fig_type,
                is_visible=False
            )
            fig_cards.append(new_fig_card)
        for i in range(blue_per_player):
            fig_type = blue_deck.pop(0)
            new_fig_card = FigCard(
                card_color=CardColor.BLUE,
                fig_type=fig_type,
                is_visible=False
            )
            fig_cards.append(new_fig_card)
            random.shuffle(fig_cards)
        return fig_cards, white_deck, blue_deck

    @staticmethod
    def create_mov_cards() -> List[MovCard]:
        mov_cards = []
        for i in range(3):
            new_mov_card = MovCard(mov_type=random.choice(list(MovType)))
            mov_cards.append(new_mov_card)
        return mov_cards

    def get_player_by_name(self, player_name) -> Player | None:
        for player in self.players:
            if player.player_name == player_name:
                return player
        return None
