from collections import Counter
from app.models.board import Board
from app.models.tile import TileColor 
from uuid import uuid1

try:
    match_id = uuid1()
    board = Board()
except ValueError as e:
    print(f"Error: {e}")

def test_board_size():
    # Verify there are 36 tiles
    assert len(board.tiles) == 36, f"Expected 36 tiles, found {len(board.tiles)}"

def test_dup_tiles():            
    # Verify any tile has a same position
    positions = [(tile.tile_pos_x, tile.tile_pos_y) for tile in board.tiles]
    unique_positions = set(positions)
    assert len(positions) == len(unique_positions), "Found tiles with duplicate positions (both x and y)"

def test_range_tiles(): 
    # Verify all tile positions are in range [0,6)
    positions = [(tile.tile_pos_x, tile.tile_pos_y) for tile in board.tiles]    
    for pos_x, pos_y in positions:
        assert 0 <= pos_x <= 5, f"Tile pos_x {pos_x} out of range"
        assert 0 <= pos_y <= 5, f"Tile pos_y {pos_y} out of range"
            
def test_board_colors():
    # Verify there are 9 tiles for each color
    color_counts = Counter(tile.tile_color for tile in board.tiles)
    assert color_counts[TileColor.RED] == 9, f"Expected 9 red tiles, found {color_counts[TileColor.RED]}"
    assert color_counts[TileColor.YELLOW] == 9, f"Expected 9 yellow tiles, found {color_counts[TileColor.YELLOW]}"
    assert color_counts[TileColor.GREEN] == 9, f"Expected 9 green tiles, found {color_counts[TileColor.GREEN]}"
    assert color_counts[TileColor.BLUE] == 9, f"Expected 9 blue tiles, found {color_counts[TileColor.BLUE]}"

