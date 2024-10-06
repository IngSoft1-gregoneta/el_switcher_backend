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
            match_out = fige01_detector(match_out, x, y)
            match_out = fige03_detector(match_out, x, y)
            match_out = fige05_detector(match_out, x, y)
            match_out = fige07_detector(match_out, x, y)
    match_repo.update_match(match_out)

def fige01_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fige01_rot1_detector(match_out, x, y)
    match_out = fige01_rot2_detector(match_out, x, y)
    return match_out

def fige01_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige01_rot1_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        up_right = (center_x+1, center_y-1)
        left = (center_x-1, center_y)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(left[0], left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fige01.value
    return match_out

def fige01_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x+1<columns and center_x-1>=0

def fige01_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige01_rot2_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        up_right = (center_x+1, center_y+1)
        left = (center_x, center_y-1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(up_right[0], up_right[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(left[0], left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(up_right[0], up_right[1])].tile_in_figure = FigType.fige01.value
            match_out.board.tiles[coordinates_to_index(left[0], left[1])].tile_in_figure = FigType.fige01.value
    return match_out
        
def fige01_rot2_verifications(center_x: int, center_y: int):
    return center_y+1<columns and center_y-1>=0 and center_x+1<columns

def fige03_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fige03_rot1_detector(match_out, x, y)
    match_out = fige03_rot2_detector(match_out, x, y)
    return match_out

def fige03_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige03_rot1_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        up_left = (center_x-1, center_y-1)
        right = (center_x+1, center_y)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(right[0], right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fige03.value
    return match_out

def fige03_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x+1<columns and center_x-1>=0

def fige03_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige03_rot2_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        up_left = (center_x+1, center_y-1)
        right = (center_x, center_y+1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(up_left[0], up_left[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(right[0], right[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(up_left[0], up_left[1])].tile_in_figure = FigType.fige03.value
            match_out.board.tiles[coordinates_to_index(right[0], right[1])].tile_in_figure = FigType.fige03.value
    return match_out
        
def fige03_rot2_verifications(center_x: int, center_y: int):
    return center_y+1<columns and center_y-1>=0 and center_x+1<columns


def fige05_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    match_out = match
    match_out = fige05_rot1_detector(match_out, x, y)
    match_out = fige05_rot2_detector(match_out, x, y)
    match_out = fige05_rot3_detector(match_out, x, y)
    match_out = fige05_rot4_detector(match_out, x, y)
    return match_out

def fige05_rot1_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige05_rot1_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        down = (center_x, center_y+1)
        down_left = (center_x-1, center_y+1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
    return match_out

def fige05_rot1_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<columns and center_x-1>=0

def fige05_rot2_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige05_rot2_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x-1, center_y)
        down = (center_x+1, center_y)
        down_left = (center_x+1, center_y+1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
    return match_out
        
def fige05_rot2_verifications(center_x: int, center_y: int):
    return center_y+1<columns and center_x-1>=0 and center_x+1<columns

def fige05_rot3_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige05_rot3_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x, center_y-1)
        down = (center_x, center_y+1)
        down_left = (center_x+1, center_y-1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
    return match_out

def fige05_rot3_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_y+1<columns and center_x+1<columns

def fige05_rot4_detector(match: MatchOut, x: int, y: int) -> MatchOut:
    center_x = x
    center_y = y
    match_out = match
    if match is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
    if (fige05_rot4_verifications(center_x, center_y)):
        color = match_out.board.tiles[coordinates_to_index(x, y)].tile_color
        up = (center_x+1, center_y)
        down = (center_x-1, center_y)
        down_left = (center_x-1, center_y-1)
        if match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_color == color and \
        match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
            match_out.board.tiles[coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
            match_out.board.tiles[coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
    return match_out
        
def fige05_rot4_verifications(center_x: int, center_y: int):
    return center_y-1>=0 and center_x-1>=0 and center_x+1<columns

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
