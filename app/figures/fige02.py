import figure_detector
from utils.match_handler import *

def fige02_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige02_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        up_right = (center_x+1, center_y-1)
        right = (center_x+1, center_y)
        if match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige02.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige02.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fige02.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fige02.value
    return match_out

def fige02_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x+1<figure_detector.columns
