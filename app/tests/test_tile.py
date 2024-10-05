from models.tile import Tile, TileColor, FigType

def test_valid_tile_color_enum():
    # Verify tile created in a normal case
    tile = None 
    tile_color = TileColor.RED 
    tile_pos_x = 0
    tile_pos_y = 5
    try:
        tile = Tile(tile_color=tile_color, tile_in_figure=FigType.none, tile_pos_x=tile_pos_x, tile_pos_y=tile_pos_y)
        assert tile.tile_color == tile_color, f"{tile.tile_color} is not a valid color"
        assert tile.tile_pos_x == tile_pos_x, f"x={tile.tile_color} is not a valid pos"
        assert tile.tile_pos_y == tile_pos_y, f"y={tile.tile_color} is not a valid pos"
    except ValueError as e:
        assert False

def test_valid_tile_color_str():
    # Verify tile created in a normal case but color input was a str and not a color enum 
    tile = None 
    tile_color = 'Yellow'
    tile_pos_x = 0
    tile_pos_y = 5
    try:
        tile = Tile(tile_color=tile_color, tile_in_figure=FigType.none, tile_pos_x=tile_pos_x, tile_pos_y=tile_pos_y)
        assert tile.tile_color == TileColor.YELLOW, f"{tile.tile_color} is not a valid color"
        assert tile.tile_pos_x == tile_pos_x, f"x={tile.tile_color} is not a valid pos"
        assert tile.tile_pos_y == tile_pos_y, f"y={tile.tile_color} is not a valid pos"
    except ValueError as e:
        assert False

def test_bad_color_str():
    # Verify tile doesn't created with a wrong color
    tile = None 
    tile_color = 'Purple'
    tile_pos_x = 1
    tile_pos_y = 5
    try:
        tile = Tile(tile_color=tile_color, tile_in_figure=FigType.none, tile_pos_x=tile_pos_x, tile_pos_y=tile_pos_y)
        assert False, f"{tile.tile_color} is not a valid color"
    except ValueError as e:
        assert tile == None
        
def test_bad_pos():
    # Verify tile doesn't created with a wrong position
    tile = None 
    tile_color = TileColor.BLUE
    tile_pos_x = 1
    tile_pos_y = 6
    try:
        tile = Tile(tile_color=tile_color, tile_in_figure=FigType.none, tile_pos_x=tile_pos_x, tile_pos_y=tile_pos_y)
        assert False, f"({tile.tile_pos_x},{tile.tile_pos_x}) is not a valid position"
    except ValueError as e:
        assert tile == None
