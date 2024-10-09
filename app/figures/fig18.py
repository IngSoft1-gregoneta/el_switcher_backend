import figure_detector
from match_handler import *

def fig18_detector(board: Board, x: int, y: int) -> Board:
    board_out = board
    board_out = fig18_rot1_detector(board_out, x, y)
    board_out = fig18_rot2_detector(board_out, x, y)
    board_out = fig18_rot3_detector(board_out, x, y)
    board_out = fig18_rot4_detector(board_out, x, y)
    return board_out

def fig18_rot1_detector(board: Board, x: int, y: int) -> Board:
    center_x = x
    center_y = y
    board_out = board
    if board is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="board not found")
    if (fig18_rot1_verifications(center_x, center_y)):
        color = board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        up_left = (center_x-1, center_y-1)
        up_right = (center_x+1, center_y-1)
        right = (center_x+1, center_y)
        if board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        fig18_rot1_borders_verifications(center_x, center_y, board, color):
            board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig18.value
    return board_out

def fig18_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x-1>=0 and center_x+1<figure_detector.columns

def fig18_rot1_borders_verifications(center_x: int, center_y: int, board: Board, color: TileColor):
    valid = True
    border1 = (center_x-1, center_y-2)
    border2 = (center_x, center_y-2)
    border3 = (center_x+1, center_y-2)
    border4 = (center_x+2, center_y-1)
    border5 = (center_x+2, center_y)
    border6 = (center_x+1, center_y+1)
    border7 = (center_x, center_y+1)
    border8 = (center_x-1, center_y)
    border9 = (center_x-2, center_y-1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid

def fig18_rot2_detector(board: Board, x: int, y: int) -> Board:
    center_x = x
    center_y = y
    board_out = board
    if board is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="board not found")
    if (fig18_rot2_verifications(center_x, center_y)):
        color = board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x-1, center_y)
        up_left = (center_x-1, center_y+1)
        up_right = (center_x-1, center_y-1)
        right = (center_x, center_y-1)
        if board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        fig18_rot2_borders_verifications(center_x, center_y, board, color):
            board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig18.value
    return board_out

def fig18_rot2_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<figure_detector.columns and center_x-1>=0

def fig18_rot2_borders_verifications(center_x: int, center_y: int, board: Board, color: TileColor):
    valid = True
    border1 = (center_x-2, center_y+1)
    border2 = (center_x-2, center_y)
    border3 = (center_x-2, center_y-1)
    border4 = (center_x-1, center_y-2)
    border5 = (center_x, center_y-2)
    border6 = (center_x+1, center_y-1)
    border7 = (center_x+1, center_y)
    border8 = (center_x, center_y+1)
    border9 = (center_x-1, center_y+2)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid

def fig18_rot3_detector(board: Board, x: int, y: int) -> Board:
    center_x = x
    center_y = y
    board_out = board
    if board is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="board not found")
    if (fig18_rot3_verifications(center_x, center_y)):
        color = board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y+1)
        up_left = (center_x+1, center_y+1)
        up_right = (center_x-1, center_y+1)
        right = (center_x-1, center_y)
        if board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        fig18_rot3_borders_verifications(center_x, center_y, board, color):
            board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig18.value
    return board_out

def fig18_rot3_verifications(center_x: int, center_y: int):
    return center_y+1<figure_detector.columns and center_x-1>=0 and center_x+1<figure_detector.columns

def fig18_rot3_borders_verifications(center_x: int, center_y: int, board: Board, color: TileColor):
    valid = True
    border1 = (center_x+1, center_y+2)
    border2 = (center_x, center_y+2)
    border3 = (center_x-1, center_y+2)
    border4 = (center_x-2, center_y+1)
    border5 = (center_x-2, center_y)
    border6 = (center_x-1, center_y-1)
    border7 = (center_x, center_y-1)
    border8 = (center_x+1, center_y)
    border9 = (center_x+2, center_y+1)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid

def fig18_rot4_detector(board: Board, x: int, y: int) -> Board:
    center_x = x
    center_y = y
    board_out = board
    if board is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="board not found")
    if (fig18_rot4_verifications(center_x, center_y)):
        color = board.tiles[figure_detector.coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        up_left = (center_x+1, center_y-1)
        up_right = (center_x+1, center_y+1)
        right = (center_x, center_y+1)
        if board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_color == color and \
        fig18_rot4_borders_verifications(center_x, center_y, board, color):
            board.tiles[figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fig18.value
            board.tiles[figure_detector.coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fig18.value
    return board_out

def fig18_rot4_verifications(center_x: int, center_y: int):
    return  center_y-1>=0 and center_y+1<figure_detector.columns and center_x+1<figure_detector.columns

def fig18_rot4_borders_verifications(center_x: int, center_y: int, board: Board, color: TileColor):
    valid = True
    border1 = (center_x+2, center_y-1)
    border2 = (center_x+2, center_y)
    border3 = (center_x+2, center_y+1)
    border4 = (center_x+1, center_y+2)
    border5 = (center_x, center_y+2)
    border6 = (center_x-1, center_y+1)
    border7 = (center_x-1, center_y)
    border8 = (center_x, center_y-1)
    border9 = (center_x+1, center_y-2)
    if border1[0] >= 0 and border1[0]<figure_detector.columns and \
    border1[1] >= 0 and border1[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border1[0], border1[1])].tile_color != color
    if border2[0] >= 0 and border2[0]<figure_detector.columns and \
    border2[1] >= 0 and border2[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border2[0], border2[1])].tile_color != color
    if border3[0] >= 0 and border3[0]<figure_detector.columns and \
    border3[1] >= 0 and border3[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border3[0], border3[1])].tile_color != color
    if border4[0] >= 0 and border4[0]<figure_detector.columns and \
    border4[1] >= 0 and border4[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border4[0], border4[1])].tile_color != color
    if border5[0] >= 0 and border5[0]<figure_detector.columns and \
    border5[1] >= 0 and border5[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border5[0], border5[1])].tile_color != color
    if border6[0] >= 0 and border6[0]<figure_detector.columns and \
    border6[1] >= 0 and border6[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border6[0], border6[1])].tile_color != color
    if border7[0] >= 0 and border7[0]<figure_detector.columns and \
    border7[1] >= 0 and border7[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border7[0], border7[1])].tile_color != color
    if border8[0] >= 0 and border8[0]<figure_detector.columns and \
    border8[1] >= 0 and border8[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border8[0], border8[1])].tile_color != color
    if border9[0] >= 0 and border9[0]<figure_detector.columns and \
    border9[1] >= 0 and border9[1]<figure_detector.columns: 
        valid = valid and \
        board.tiles[figure_detector.coordinates_to_index(border9[0], border9[1])].tile_color != color
    return valid
