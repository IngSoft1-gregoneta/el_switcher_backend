import figure_detector
from utils.match_handler import *

def fig05_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fig05_rot1_detector(match_out, x, y)
    match_out = fig05_rot2_detector(match_out, x, y)
    return match_out

def fig05_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig05_rot1_verifications(center_x)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x-1, center_y)
        left2 = (center_x-2, center_y)
        right = (center_x+1, center_y)
        right2 = (center_x+2, center_y)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left2[0], left2[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right2[0], right2[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left2[0], left2[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right2[0], right2[1])].tile_in_figure = FigType.fig05.value
    return match_out

def fig05_rot1_verifications(center_x: int):
    return center_x-2>=0 and center_x+2<figure_detector.columns

def fig05_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig05_rot2_verifications(center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x, center_y+1)
        left2 = (center_x, center_y+2)
        right = (center_x, center_y-1)
        right2 = (center_x, center_y-2)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left2[0], left2[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right2[0], right2[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left2[0], left2[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig05.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right2[0], right2[1])].tile_in_figure = FigType.fig05.value
    return match_out

def fig05_rot2_verifications(center_y: int):
    return center_y+2<figure_detector.columns and center_y-2>=0
