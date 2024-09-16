import random
from typing import List
from tile_model import Tile

class Board:
    def __init__(self, game_id):
        self.game_id: int = game_id
        self.tiles: List[Tile] = self._crear_fichas()

    def _crear_fichas(self) -> List[Tile]:
        # Define colorsand create list of 9 tiles for each color
        colors = ['red', 'yellow', 'green', 'blue']
        color_list = colors * 9
                
        # Create tiles in random pos
        random.shuffle(color_list)
        tiles = []
        for i in range(36):
         color = color_list[i]
         tile = Tile(
             tile_color=color,
             tile_pos_x = i % 6,   
             tile_pos_y = i // 6
         )
         tiles.append(tile)
        return tiles

    # for debug
    def print_board(self):
        print(f"board:\ngame id: {self.game_id}")
        for tile in self.tiles:
            print(tile)

# Create a board instance and print files
# board = Board(game_id=1)
# board.print_board()