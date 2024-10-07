import figure_detector
from utils.match_handler import *

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
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        down = (center_x, center_y+1)
        down_right = (center_x+1, center_y+1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_color == color and \
        fige07_rot1_borders_verifications(center_x, center_y, match, color):
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out

def fige07_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<figure_detector.columns and center_x+1<figure_detector.columns

def fige07_rot1_borders_verifications(center_x: int, center_y: int, match: MatchOut, color: TileColor):
    valid = True
    border1 = (center_x, center_y-2)
    border2 = (center_x+1, center_y-1)
    border3 = (center_x+1, center_y)
    border4 = (center_x+2, center_y+1)
    border5 = (center_x+1, center_y+2)
    border6 = (center_x, center_y+2)
    border7 = (center_x-1, center_y+1)
    border8 = (center_x-1, center_y)
    border9 = (center_x-1, center_y-1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid

def fige07_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot2_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x-1, center_y)
        down = (center_x+1, center_y)
        down_right = (center_x+1, center_y-1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_color == color and \
        fige07_rot2_borders_verifications(center_x, center_y, match, color):
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out
        
def fige07_rot2_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x-1>=0 and center_x+1<figure_detector.columns

def fige07_rot2_borders_verifications(center_x: int, center_y: int, match: MatchOut, color: TileColor):
    valid = True
    border1 = (center_x-2, center_y)
    border2 = (center_x-1, center_y-1)
    border3 = (center_x, center_y-1)
    border4 = (center_x+1, center_y-2)
    border5 = (center_x+2, center_y-1)
    border6 = (center_x+2, center_y)
    border7 = (center_x+1, center_y+1)
    border8 = (center_x, center_y+1)
    border9 = (center_x-1, center_y+1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid


def fige07_rot3_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot3_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y+1)
        down = (center_x, center_y-1)
        down_right = (center_x-1, center_y-1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_color == color and \
        fige07_rot3_borders_verifications(center_x, center_y, match, color):
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out

def fige07_rot3_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<figure_detector.columns and center_x-1>=0

def fige07_rot3_borders_verifications(center_x: int, center_y: int, match: MatchOut, color: TileColor):
    valid = True
    border1 = (center_x, center_y+2)
    border2 = (center_x-1, center_y+1)
    border3 = (center_x-1, center_y)
    border4 = (center_x-2, center_y-1)
    border5 = (center_x-1, center_y-2)
    border6 = (center_x, center_y-2)
    border7 = (center_x+1, center_y-1)
    border8 = (center_x+1, center_y)
    border9 = (center_x+1, center_y+1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid


def fige07_rot4_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige07_rot4_verifications(center_x, center_y)):
        color = match_out.board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        down = (center_x-1, center_y)
        down_right = (center_x-1, center_y+1)
        if match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_color == color and \
        fige07_rot4_borders_verifications(center_x, center_y, match, color):
            match_out.board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige07.value
            match_out.board.tiles[figure_detector.coordinates_to_index(down_right[0], down_right[1])].tile_in_figure = FigType.fige07.value
    return match_out
        
def fige07_rot4_verifications(center_x: int, center_y: int):
    return center_y+1<figure_detector.columns and center_x-1>=0 and center_x+1<figure_detector.columns

def fige07_rot4_borders_verifications(center_x: int, center_y: int, match: MatchOut, color: TileColor):
    valid = True
    border1 = (center_x+2, center_y)
    border2 = (center_x+1, center_y+1)
    border3 = (center_x, center_y+1)
    border4 = (center_x-1, center_y+2)
    border5 = (center_x-2, center_y+1)
    border6 = (center_x-2, center_y)
    border7 = (center_x-1, center_y-1)
    border8 = (center_x, center_y-1)
    border9 = (center_x+1, center_y-1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        match.board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid
