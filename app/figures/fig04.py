import figure_detector
from utils.match_handler import *

def fig04_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fig04_rot1_detector(match_out, x, y)
    match_out = fig04_rot2_detector(match_out, x, y)
    match_out = fig04_rot3_detector(match_out, x, y)
    match_out = fig04_rot4_detector(match_out, x, y)
    return match_out

def fig04_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig04_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x-1, center_y)
        left_up = (center_x-1, center_y-1)
        down = (center_x, center_y+1)
        right_down = (center_x+1, center_y+1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_in_figure = FigType.fig04.value
    return match_out

def fig04_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig04_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x, center_y+1)
        left_up = (center_x-1, center_y+1)
        down = (center_x+1, center_y)
        right_down = (center_x+1, center_y-1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_in_figure = FigType.fig04.value
    return match_out
       
def fig04_rot3_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig04_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x+1, center_y)
        left_up = (center_x+1, center_y+1)
        down = (center_x, center_y-1)
        right_down = (center_x-1, center_y-1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_in_figure = FigType.fig04.value
    return match_out
        
def fig04_rot4_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fig04_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        left = (center_x, center_y-1)
        left_up = (center_x+1, center_y-1)
        down = (center_x-1, center_y)
        right_down = (center_x-1, center_y+1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_color == color:
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(left_up[0], left_up[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fig04.value
            match_out.board.tiles[figure_detector.coordinates_to_index(right_down[0], right_down[1])].tile_in_figure = FigType.fig04.value
    return match_out


def fig04_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<figure_detector.columns and center_x-1>=0 and center_x+1<figure_detector.columns
