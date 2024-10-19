from enum import Enum
from pydantic import BaseModel
from .fig_card import FigType
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
            raise ValueError(f"{self.tile_color} no es un TileColor valido")
        if self.tile_pos_x not in range(0, 6) or self.tile_pos_y not in range(0, 6):
            raise ValueError(f"({self.tile_pos_x}, {self.tile_pos_y}) no es una posicion valida en el tablero")
        if self.tile_in_figure.value != "None":
            raise ValueError("La ficha inicial no forma una figura")