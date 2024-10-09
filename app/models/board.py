import random
from typing import List
from pydantic import BaseModel
from .tile import *
from uuid import UUID 

AMOUNT_OF_TILES = 36

class Board(BaseModel):
    tiles: List[Tile]

    def __init__(self):
        tiles = self._create_tiles()
        super().__init__(tiles=tiles)

    def _create_tiles(self) -> List[Tile]:
        # Define colors and create list of 9 tiles for each color
        colors = [TileColor.RED, TileColor.YELLOW, TileColor.GREEN, TileColor.BLUE]
        color_list = colors * (AMOUNT_OF_TILES // len(colors))
                
        # Create tiles in random positions
        random.shuffle(color_list)
        tiles = []
        for i in range(AMOUNT_OF_TILES):
            color = color_list[i]
            tile = Tile(
                tile_color=color,
                tile_pos_x=i % AMOUNT_OF_TILES ** 0.5,
                tile_pos_y=i // AMOUNT_OF_TILES ** 0.5
            )
            tiles.append(tile)
        return tiles
