from app.figure_detector import *

def fige07_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fige07_rot1_detector(match_out, x, y)
    match_out = fige07_rot2_detector(match_out, x, y)
    match_out = fige07_rot3_detector(match_out, x, y)
    match_out = fige07_rot4_detector(match_out, x, y)
    return match_out

def fige07_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot1_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        down = (center_x, center_y+1)
        down_right = (center_x+1, center_y+1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out

def fige07_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<columns and center_x+1<columns

def fige07_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot2_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x-1, center_y)
        down = (center_x+1, center_y)
        down_right = (center_x+1, center_y-1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out
        
def fige07_rot2_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x-1>=0 and center_x+1<columns

def fige07_rot3_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot3_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y+1)
        down = (center_x, center_y-1)
        down_right = (center_x-1, center_y-1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out

def fige07_rot3_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<columns and center_x-1>=0

def fige07_rot4_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot4_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        down = (center_x-1, center_y)
        down_right = (center_x-1, center_y+1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out
        
def fige07_rot4_verifications(center_x: int, center_y: int):
    return center_y+1<columns and center_x-1>=0 and center_x+1<columns
