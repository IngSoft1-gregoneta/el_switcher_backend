from enum import Enum

class TileColor(Enum):
    RED = 'Red'
    YELLOW = 'Yellow'
    GREEN = 'Green'
    BLUE = 'Blue'

class Tile():

    def __init__(self, tile_color, tile_pos_x, tile_pos_y):
        self.tile_color: TileColor = tile_color
        self.tile_pos_x: int = tile_pos_x  
        self.tile_pos_y: int = tile_pos_y
        self.valid_tile()

    def valid_tile(self):
        if self.tile_color not in TileColor.__members__.values():
            raise ValueError(f"{self.tile_color} is not a TileColor")
        if self.tile_pos_x not in range(0,6) or self.tile_pos_y not in range(0,6):
            raise ValueError(f"({self.tile_pos_x},{self.tile_pos_y}) is not a valid pos in board")
        
    def print_tile(self):
        print(f"color: {self.tile_color.value}, pos_x: {self.tile_pos_x}, pos_y: {self.tile_pos_y}")

# Example usage:
"""
try:
    tile = Tile(tile_color=TileColor.RED, tile_pos_x=0, tile_pos_y=5)
    tile.print_tile()
except ValueError as e:
    print(f"Error: {e}")

try:
    tile = Tile(tile_color=TileColor.RED, tile_pos_x=0, tile_pos_y=6)
    tile.print_tile()
except ValueError as e:
    print(f"Error: {e}")

try:
    tile = Tile(tile_color='Red', tile_pos_x=0, tile_pos_y=5)
    tile.print_tile()
except ValueError as e:
    print(f"Error: {e}")
"""