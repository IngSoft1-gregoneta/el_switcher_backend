from app.models.visible_match import VisibleMatchData
from models.match import * 
from figures import fige01, fige02, fige03, fige04, fige05, fige06, fige07, \
    fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08
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

# las subfiguras de otras figuras no pueden tomar fichas de la superfigura
def figures_detector(match: MatchOut):
    match_out = match
    fig_types = get_valid_fig_types(match)
    for y in range(columns):
        for x in range(columns):
            detect_fige01(match_out, fig_types, x, y)
            detect_fige02(match_out, fig_types, x, y)
            detect_fige03(match_out, fig_types, x, y)
            detect_fige04(match_out, fig_types, x, y)
            detect_fige05(match_out, fig_types, x, y)
            detect_fige06(match_out, fig_types, x, y)
            detect_fige07(match_out, fig_types, x, y)
            detect_fig01(match_out, fig_types, x, y)
            detect_fig02(match_out, fig_types, x, y)
            detect_fig03(match_out, fig_types, x, y)
            detect_fig04(match_out, fig_types, x, y)
            detect_fig05(match_out, fig_types, x, y)
            detect_fig06(match_out, fig_types, x, y)
            detect_fig07(match_out, fig_types, x, y)
            detect_fig08(match_out, fig_types, x, y)
    match_repo.update_match(match_out)

def get_valid_fig_types(match: MatchOut) -> List[str]:
    fig_types: List[str] = []    
    visible_data = VisibleMatchData(match.match_id,match.players[0].player_name)
    visible_fig_cards = visible_data.me.visible_fig_cards 
    for other_player in visible_data.other_players: 
        visible_fig_cards = visible_fig_cards + other_player.visible_fig_cards
    for fig_card in visible_fig_cards:
        fig_types.append(fig_card.fig_type)
    return fig_types

def detect_fige01(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige01.value in fig_types:
        match = fige01.fige01_detector(match, x, y)

def detect_fige02(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige02.value in fig_types:
        match = fige02.fige02_detector(match, x, y)

def detect_fige03(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige03.value in fig_types:
        match = fige03.fige03_detector(match, x, y)

def detect_fige04(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige04.value in fig_types:
        match = fige04.fige04_detector(match, x, y)

def detect_fige05(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige05.value in fig_types:
        match = fige05.fige05_detector(match, x, y)

def detect_fige06(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige06.value in fig_types:
        match = fige06.fige06_detector(match, x, y)

def detect_fige07(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fige07.value in fig_types:
        match = fige07.fige07_detector(match, x, y)

def detect_fig01(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig01.value in fig_types:
        match = fig01.fig01_detector(match, x, y)

def detect_fig02(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig02.value in fig_types:
        match = fig02.fig02_detector(match, x, y)
    
def detect_fig03(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig03.value in fig_types:
        match = fig03.fig03_detector(match, x, y)

def detect_fig04(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig04.value in fig_types:
        match = fig04.fig04_detector(match, x, y)

def detect_fig05(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig05.value in fig_types:
        match = fig05.fig05_detector(match, x, y)

def detect_fig06(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig06.value in fig_types:
        match = fig06.fig06_detector(match, x, y)

def detect_fig07(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig07.value in fig_types:
        match = fig07.fig07_detector(match, x, y)

def detect_fig08(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig08.value in fig_types:
        match = fig08.fig08_detector(match, x, y)