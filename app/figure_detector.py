from models.match import * 

# primero vamos a hacer las figuras blancas
match_repo = MatchRepository()
columns = int(AMOUNT_OF_TILES ** 0.5)

# asumimos que siempre los indices de tiles en board y las posiciones de las tiles son consistentes
# board[0] => tile.x = 0, tile.y = 0, ...,  board[35] => tile.x = 5, tile.y = 5

def coordinates_to_index(x: int, y: int) -> int:
    if 0 <= x < columns and 0 <= y < columns:
        return y * columns + x
    else:
        raise ValueError("coordinates must be in range 0 to 5")

def index_to_coordinates(index: int) -> tuple[int, int]:
    if 0 <= index < columns * columns:
        y = index // columns
        x = index % columns
        return (x, y)
    else:
        raise ValueError("Tile index in board must be in range 0 to 35")

def figures_detector(match: MatchOut):
    match_out = match
    for y in range(columns):
        for x in range(columns):
            match_out = fig01_detector(match_out, x, y)
            print()
    match_repo.update_match(match_out)

def fig01_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = fig01_rot1_detector(match, x, y)
    return match_out
             
def fig01_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if (fig01_rot1_verifications(center_x, center_y)):
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up_y = center_y-1
        down_y = center_y+1
        right_x = center_x+1
        print(f"center_x: {center_x}, center_y: {center_y}")
        print(match_out.board.tiles[coordinates_to_index(center_x, up_y)].tile_color )
        print(match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_color )
        print(match_out.board.tiles[coordinates_to_index(center_x, down_y)].tile_color)
        print(match_out.board.tiles[coordinates_to_index(right_x, down_y)].tile_color)
        if match_out.board.tiles[coordinates_to_index(center_x, up_y)].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(center_x, down_y)].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(right_x, down_y)].tile_color == color:
            print("actualizando tiles")
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fig01.value
            match_out.board.tiles[coordinates_to_index(center_x, up_y)].tile_in_figure = FigType.fig01.value
            match_out.board.tiles[coordinates_to_index(center_x, down_y)].tile_in_figure = FigType.fig01.value
            match_out.board.tiles[coordinates_to_index(right_x, down_y)].tile_in_figure = FigType.fig01.value
    return match_out
        

def fig01_rot1_verifications(x: int, y: int):
    return y-1>=0 and y+1<columns and x+1<columns