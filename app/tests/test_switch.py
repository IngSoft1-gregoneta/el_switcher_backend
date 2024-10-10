from app import switcher
from switcher import *

def test_invalid_switch_mov1():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    print()
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y - 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov1.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov1():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 2
    y1 = y - 2
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x + 2
    y2 = y - 2
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x - 2
    y3 = y + 2
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x + 2
    y4 = y + 2
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov1.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov1.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov1.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov1.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov1.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov1.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov1.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov1.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color


def test_invalid_switch_mov2():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y - 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov2.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov2():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 2
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x
    y2 = y - 2
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x + 2
    y3 = y
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x - 2
    y4 = y
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov2.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov2.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov2.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov2.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov2.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov2.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov2.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov2.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color

def test_invalid_switch_mov3():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y - 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov3.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov3():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x
    y2 = y - 1
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x + 1
    y3 = y
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x - 1
    y4 = y
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov3.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov3.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov3.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov3.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov3.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov3.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov3.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov3.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color

def test_invalid_switch_mov4():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov4.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov4():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y - 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x + 1
    y2 = y - 1
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x - 1
    y3 = y + 1
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x + 1
    y4 = y + 1
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov4.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov4.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov4.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov4.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov4.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov4.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov4.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov4.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color

def test_invalid_switch_mov5():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov5.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov5():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 2
    y1 = y - 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x + 1
    y2 = y - 2
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x + 2
    y3 = y + 1
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x - 1
    y4 = y + 2
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov5.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov5.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov5.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov5.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov5.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov5.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov5.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov5.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color


def test_invalid_switch_mov6():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x - 1
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov6.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov6():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 2
    y = 3
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x - 2
    y1 = y + 1
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x - 1
    y2 = y - 2
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    x3 = x + 2
    y3 = y - 1
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x + 1
    y4 = y + 2
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov6.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov6.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov6.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov6.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    switcher.switch(board, MovType.mov6.value, x, y, x3, y3)
    assert tile.tile_color == tile3_color and tile3.tile_color == tile_color
    switcher.switch(board, MovType.mov6.value, x3, y3, x, y)
    assert tile.tile_color == tile_color and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov6.value, x, y, x4, y4)
    assert tile.tile_color == tile4_color and tile4.tile_color == tile_color
    switcher.switch(board, MovType.mov6.value, x4, y4, x, y)
    assert tile.tile_color == tile_color and tile4.tile_color == tile4_color

def test_invalid_switch_mov7():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 1
    y = 1
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile.tile_color = TileColor.RED.value
    tile_color = tile.tile_color 

    x1 = x + 3
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1.tile_color = TileColor.GREEN.value
    tile1_color = tile1.tile_color

    switcher.switch(board, MovType.mov7.value, x, y, x1, y1)
    assert tile.tile_color != tile1_color and tile1.tile_color != tile_color 

def test_valid_switch_mov7():
    board = Board()

    for tile in board.tiles: tile.tile_color = tile.tile_color.value
    x = 1
    y = 1
    tile = board.tiles[switcher.coordinates_to_index(x, y)]
    tile_color = tile.tile_color 

    x1 = x + 4
    y1 = y
    tile1 = board.tiles[switcher.coordinates_to_index(x1, y1)]
    tile1_color = tile1.tile_color

    x2 = x
    y2 = y + 4
    tile2 = board.tiles[switcher.coordinates_to_index(x2, y2)]
    tile2_color = tile2.tile_color

    switcher.switch(board, MovType.mov7.value, x, y, x1, y1)
    assert tile.tile_color == tile1_color and tile1.tile_color == tile_color
    switcher.switch(board, MovType.mov7.value, x1, y1, x, y)
    assert tile.tile_color == tile_color and tile1.tile_color == tile1_color

    switcher.switch(board, MovType.mov7.value, x, y, x2, y2)
    assert tile.tile_color == tile2_color and tile2.tile_color == tile_color
    switcher.switch(board, MovType.mov7.value, x2, y2, x, y)
    assert tile.tile_color == tile_color and tile2.tile_color == tile2_color

    x_ = 4
    y_ = 4
    tile_ = board.tiles[switcher.coordinates_to_index(x_, y_)]
    tile_color_ = tile_.tile_color 

    x3 = x_ - 4
    y3 = y_
    tile3 = board.tiles[switcher.coordinates_to_index(x3, y3)]
    tile3_color = tile3.tile_color

    x4 = x_
    y4 = y_ - 4
    tile4 = board.tiles[switcher.coordinates_to_index(x4, y4)]
    tile4_color = tile4.tile_color

    switcher.switch(board, MovType.mov7.value, x_, y_, x3, y3)
    assert tile_.tile_color == tile3_color and tile3.tile_color == tile_color_
    switcher.switch(board, MovType.mov7.value, x3, y3, x_, y_)
    assert tile_.tile_color == tile_color_ and tile3.tile_color == tile3_color

    switcher.switch(board, MovType.mov7.value, x_, y_, x4, y4)
    assert tile_.tile_color == tile4_color and tile4.tile_color == tile_color_
    switcher.switch(board, MovType.mov7.value, x4, y4, x_, y_)
    assert tile_.tile_color == tile_color_ and tile4.tile_color == tile4_color

