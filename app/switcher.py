from models.board import *
from models.mov_card import *
import copy 

dim = int(AMOUNT_OF_TILES**0.5)

def switch(board: Board, mov_type: str, x1: int, y1: int, x2: int, y2: int):
    if is_valid_movement(mov_type, x1, y1, x2, y2):
        tile1 = board.tiles[coordinates_to_index(x1, y1)]
        tile2 = board.tiles[coordinates_to_index(x2, y2)]
        color1 = tile1.tile_color
        color2 = tile2.tile_color
        tile1.tile_color = color2
        tile2.tile_color = color1

def is_valid_movement(mov_type: str, x1: int, y1: int, x2: int, y2: int) -> bool:
    if pos_in_range(x1, y1) and pos_in_range(x2, y2):
        match mov_type:
            case MovType.mov1.value:
                return is_mov1_valid(x1, y1, x2, y2)
            case MovType.mov2.value:
                return is_mov2_valid(x1, y1, x2, y2)
            case MovType.mov3.value:
                return is_mov3_valid(x1, y1, x2, y2)
            case MovType.mov4.value:
                return is_mov4_valid(x1, y1, x2, y2)
            case MovType.mov5.value:
                return is_mov5_valid(x1, y1, x2, y2)
            case MovType.mov6.value:
                return is_mov6_valid(x1, y1, x2, y2)
            case MovType.mov7.value:
                return is_mov7_valid(x1, y1, x2, y2)
            case _:
                return False
    return False

def is_mov1_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-2, y1-2), (x1+2, y1-2), (x1-2, y1+2), (x1+2, y1+2)]
    return (x2, y2) in expected_pos

def is_mov2_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-2, y1), (x1, y1-2), (x1+2, y1), (x1, y1+2)]
    return (x2, y2) in expected_pos

def is_mov3_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-1, y1), (x1, y1-1), (x1+1, y1), (x1, y1+1)]
    return (x2, y2) in expected_pos

def is_mov4_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-1, y1-1), (x1+1, y1-1), (x1-1, y1+1), (x1+1, y1+1)]
    return (x2, y2) in expected_pos

def is_mov5_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-2, y1-1), (x1+1, y1-2), (x1+2, y1+1), (x1-1, y1+2)]
    return (x2, y2) in expected_pos

def is_mov6_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-2, y1+1), (x1-1, y1-2), (x1+2, y1-1), (x1+1, y1+2)]
    return (x2, y2) in expected_pos

def is_mov7_valid(x1, y1, x2, y2) -> bool:
    expected_pos = [(x1-4, y1), (x1, y1-4), (x1+4, y1), (x1, y1+4)]
    return (x2, y2) in expected_pos

def pos_in_range(x: int, y: int):
    return 0 <= x < dim and 0 <= y < dim

def coordinates_to_index(x: int, y: int) -> int:
    if 0 <= x < dim and 0 <= y < dim:
        return y * dim + x
    else:
        raise ValueError("coordinates must be in range 0 to 5")
