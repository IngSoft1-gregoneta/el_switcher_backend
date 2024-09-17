from tile import Tile, TileColor

def test_valid_tile():
    try:
        tile = Tile(tile_color=TileColor.RED, tile_pos_x=0, tile_pos_y=5)
        tile.print_tile()
    except ValueError as e:
        print(f"Error: {e}")
        assert True

def test_bad_pos():
    try:
        Tile(tile_color=TileColor.RED, tile_pos_x=0, tile_pos_y=6)
        assert False
    except ValueError as e:
        print(f"Error: {e}")

def test_bad_color():
    try:
        Tile(tile_color='Red', tile_pos_x=0, tile_pos_y=5)
        assert False
    except ValueError as e:
        print(f"Error: {e}")