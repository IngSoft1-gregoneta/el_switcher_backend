import random
from typing import List
from tile import Tile, TileColor

class Board:
    def __init__(self, game_id):
        self.game_id: int = game_id
        self.tiles: List[Tile] = self._create_tiles()

    def _create_tiles(self) -> List[Tile]:
        # Define colorsand create list of 9 tiles for each color
        colors = [TileColor.RED, TileColor.YELLOW, TileColor.GREEN, TileColor.BLUE]
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

    def print_board(self):
        print(f"board:\ngame id: {self.game_id}")
        for tile in self.tiles:
            tile.print_tile()