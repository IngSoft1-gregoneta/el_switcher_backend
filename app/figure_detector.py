from app.models.visible_match import VisibleMatchData
import copy
from models.match import * 
from figures import fige01, fige02, fige03, fige04, fige05, fige06, fige07, \
    fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, \
    fig11, fig12, fig13, fig14, fig15, fig16
match_repo = MatchRepository()
columns = int(AMOUNT_OF_TILES ** 0.5)

# asumimos que siempre los indices de tiles en board y las posiciones de las tiles son consistentes
# board[0] => tile.x = 0, tile.y = 0, ...,  board[35] => tile.x = 5, tile.y = 5

def coordinates_to_index(x: int, y: int) -> int:
    if 0 <= x < columns and 0 <= y < columns:
        return y * columns + x
    else:
        raise ValueError("coordinates must be in range 0 to 5")

def figures_detector(match: MatchOut):
    match_out = copy.deepcopy(match)
    fig_types = get_valid_fig_types(match)
    disarm_figs(match_out)
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
            detect_fig09(match_out, fig_types, x, y)
            detect_fig10(match_out, fig_types, x, y)
            detect_fig11(match_out, fig_types, x, y)
            detect_fig12(match_out, fig_types, x, y)
            detect_fig13(match_out, fig_types, x, y)
            detect_fig14(match_out, fig_types, x, y)
            detect_fig15(match_out, fig_types, x, y)
            detect_fig16(match_out, fig_types, x, y)
    return copy.deepcopy(match_out.board)

def get_valid_fig_types(match: MatchOut) -> List[str]:
    fig_types: List[str] = []    
    for player in match.players:
        for i in range(len(player.fig_cards)):
            if player.fig_cards[i].is_visible:
                fig_types.append(player.fig_cards[i].fig_type)
    return fig_types

def disarm_figs(match: MatchOut):
    for tile in match.board.tiles:
        tile.tile_in_figure = FigType.none.value

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

def detect_fig09(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig09.value in fig_types:
        match = fig09.fig09_detector(match, x, y)

def detect_fig10(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig10.value in fig_types:
        match = fig10.fig10_detector(match, x, y)

def detect_fig11(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig11.value in fig_types:
        match = fig11.fig11_detector(match, x, y)

def detect_fig12(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig12.value in fig_types:
        match = fig12.fig12_detector(match, x, y)

def detect_fig13(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig13.value in fig_types:
        match = fig13.fig13_detector(match, x, y)

def detect_fig14(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig14.value in fig_types:
        match = fig14.fig14_detector(match, x, y)

def detect_fig15(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig15.value in fig_types:
        match = fig15.fig15_detector(match, x, y)

def detect_fig16(match: MatchOut, fig_types: List[FigType], x: int, y: int) -> MatchOut:
    if FigType.fig16.value in fig_types:
        match = fig16.fig16_detector(match, x, y)