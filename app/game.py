from pydantic import BaseModel
from typing import List
from board import Board
from fig_card import FigCard, CardColor, FigType, FigTypeWhite, FigTypeBlue
from mov_card import MovCard, MovType
from player import Player
"""import random"""

# Define the Pydantic model
class Game():
    def __init__(self,game_id,players,board):
        self.game_id: int = game_id
        self.players: List[Player] = players
        self.board: Board = board

# Example usage:
"""
game_id = 1
player1 = Player(game_id=game_id, player_name="Player1", mov_cards=[], fig_cards=[])
player2 = Player(game_id=game_id, player_name="Player2", mov_cards=[], fig_cards=[])
players: List[Player] = [player1, player2]
board = Board(game_id)
fig_cards: List[FigCard] = []

# Use integer division for range to avoid float error
for i in range(50 // len(players)):
    player = players[i % len(players)]
    new_fig_card = FigCard(game_id=game_id, 
                           player_name=player.player_name,
                           card_color=CardColor.WHITE, 
                           fig_type=random.choice(list(FigTypeWhite)))
    player.fig_cards.append(new_fig_card)  # The card has a player and the player has cards

for i in range(len(3*players)):
    player = players[i % len(players)]
    new_mov_card = MovCard(game_id=game_id,
                           player_name=player.player_name,
                           mov_type=random.choice(list(MovType)))
    player.mov_cards.append(new_mov_card)

board.print_board()
for player in players:
    player.print_player()
"""