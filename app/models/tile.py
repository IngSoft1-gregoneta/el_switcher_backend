from enum import Enum
from pydantic import BaseModel
from .fig_card import FigType
from typing import Union
class TileColor(Enum):
    RED = 'Red'
    YELLOW = 'Yellow'
    GREEN = 'Green'
    BLUE = 'Blue'

class Tile(BaseModel):

    tile_color: TileColor
    tile_in_figure: FigType
    tile_pos_x: int
    tile_pos_y: int

    def __init__(self, tile_color: TileColor, tile_in_figure: FigType, tile_pos_x: int, tile_pos_y: int):
        super().__init__(tile_color=tile_color,tile_in_figure=tile_in_figure, tile_pos_x=tile_pos_x, tile_pos_y=tile_pos_y)
        self.valid_tile()

    def valid_tile(self):
        if self.tile_color not in TileColor:
            raise ValueError(f"{self.tile_color} is not a valid TileColor")
        if self.tile_pos_x not in range(0, 6) or self.tile_pos_y not in range(0, 6):
            raise ValueError(f"({self.tile_pos_x}, {self.tile_pos_y}) is not a valid position on the board")
        if self.tile_in_figure.value != "None":
            raise ValueError("Initially tile is not in a figure")