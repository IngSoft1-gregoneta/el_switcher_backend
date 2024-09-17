from typing import List
from board import Board
from fig_card import FigCard, CardColor, FigType
from mov_card import MovCard, MovType
from player import Player
import random

class Game:
    def __init__(self, game_id, players_names):
        # in
        self.game_id: int = game_id
        self.players_names: List[str] = players_names
        # out
        self.board: Board = self.create_board()
        self.players: List[Player] = self.create_players()
    
    def create_board(self):
        return Board(self.game_id)
        
    def create_players(self):
        players = []
        for player_name in self.players_names:  # Usar players_names en lugar de self.players
            fig_cards = self.create_fig_cards(len_players=len(self.players_names),
                                              game_id=self.game_id,
                                              player_name=player_name)
            mov_cards = self.create_mov_cards(game_id=self.game_id,
                                              player_name=player_name)
            player = Player(game_id=self.game_id,
                            player_name=player_name,
                            mov_cards=mov_cards,
                            fig_cards=fig_cards)
            players.append(player)
        return players

    @staticmethod
    def create_fig_cards(len_players, game_id, player_name):
        fig_cards = []
        white_figs = list(FigType)[:7]
        for i in range(50 // len_players):
            new_fig_card = FigCard(game_id=game_id, 
                           player_name=player_name,
                           card_color=CardColor.WHITE, 
                           fig_type=random.choice(white_figs))  # Solo cartas blancas por ahora
            fig_cards.append(new_fig_card)
        return fig_cards

    @staticmethod
    def create_mov_cards(game_id, player_name):
        mov_cards = []
        for i in range(3):
            new_mov_card = MovCard(game_id=game_id,
                                   player_name=player_name,
                                   mov_type=random.choice(list(MovType)))
            mov_cards.append(new_mov_card)
        return mov_cards

    def print_game(self):
        self.board.print_board()
        for player in self.players:
            player.print_player()