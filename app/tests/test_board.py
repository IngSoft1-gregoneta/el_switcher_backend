from collections import Counter
from models.board import Board
from models.tile import TileColor 
from uuid import uuid1

try:
    match_id = uuid1()
    board = Board()
except ValueError as e:
    print(f"Error: {e}")

def test_board_size():
    # Verificamos que hayan 36 fichas
    assert len(board.tiles) == 36, f"Se esperaban 36 fichas, cantidad actual: {len(board.tiles)}"

def test_dup_tiles():            
    # Verificamos que cada ficha tenga una unica posicion
    positions = [(tile.tile_pos_x, tile.tile_pos_y) for tile in board.tiles]
    unique_positions = set(positions)
    assert len(positions) == len(unique_positions), "Se encontraron fichas con posiciones iguales (en x & en y)"

def test_range_tiles(): 
    # Verificamos que todas las posiciones sean del rango [0,6)
    positions = [(tile.tile_pos_x, tile.tile_pos_y) for tile in board.tiles]    
    for pos_x, pos_y in positions:
        assert 0 <= pos_x <= 5, f"Tile pos_x {pos_x} out of range"
        assert 0 <= pos_y <= 5, f"Tile pos_y {pos_y} out of range"
            
def test_board_colors():
    # Verificamos que haya 9 fichas por color
    color_counts = Counter(tile.tile_color for tile in board.tiles)
    assert color_counts[TileColor.RED] == 9, f"Expected 9 red tiles, found {color_counts[TileColor.RED]}"
    assert color_counts[TileColor.YELLOW] == 9, f"Expected 9 yellow tiles, found {color_counts[TileColor.YELLOW]}"
    assert color_counts[TileColor.GREEN] == 9, f"Expected 9 green tiles, found {color_counts[TileColor.GREEN]}"
    assert color_counts[TileColor.BLUE] == 9, f"Expected 9 blue tiles, found {color_counts[TileColor.BLUE]}"

