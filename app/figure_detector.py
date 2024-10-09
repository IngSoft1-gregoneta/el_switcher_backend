import copy
from models.match import * 
from figures import fige01, fige02, fige03, fige04, fige05, fige06, fige07, \
    fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, \
    fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18
match_repo = MatchRepository()
columns = int(AMOUNT_OF_TILES ** 0.5)

# asumimos que siempre los indices de tiles en board y las posiciones de las tiles son consistentes
# board[0] => tile.x = 0, tile.y = 0, ...,  board[35] => tile.x = 5, tile.y = 5

def coordinates_to_index(x: int, y: int) -> int:
    if 0 <= x < columns and 0 <= y < columns:
        return y * columns + x
    else:
        raise ValueError("coordinates must be in range 0 to 5")

def figures_detector(board: Board, fig_types: List[str]) -> Board:
    board_out = copy.deepcopy(board)
    disarm_figs(board_out)
    for y in range(columns):
        for x in range(columns):
            detect_fige01(board_out, fig_types, x, y)
            detect_fige02(board_out, fig_types, x, y)
            detect_fige03(board_out, fig_types, x, y)
            detect_fige04(board_out, fig_types, x, y)
            detect_fige05(board_out, fig_types, x, y)
            detect_fige06(board_out, fig_types, x, y)
            detect_fige07(board_out, fig_types, x, y)
            detect_fig01(board_out, fig_types, x, y)
            detect_fig02(board_out, fig_types, x, y)
            detect_fig03(board_out, fig_types, x, y)
            detect_fig04(board_out, fig_types, x, y)
            detect_fig05(board_out, fig_types, x, y)
            detect_fig06(board_out, fig_types, x, y)
            detect_fig07(board_out, fig_types, x, y)
            detect_fig08(board_out, fig_types, x, y)
            detect_fig09(board_out, fig_types, x, y)
            detect_fig10(board_out, fig_types, x, y)
            detect_fig11(board_out, fig_types, x, y)
            detect_fig12(board_out, fig_types, x, y)
            detect_fig13(board_out, fig_types, x, y)
            detect_fig14(board_out, fig_types, x, y)
            detect_fig15(board_out, fig_types, x, y)
            detect_fig16(board_out, fig_types, x, y)
            detect_fig17(board_out, fig_types, x, y)
            detect_fig18(board_out, fig_types, x, y)
    return copy.deepcopy(board_out)


def disarm_figs(board: Board):
    for tile in board.tiles:
        tile.tile_in_figure = FigType.none.value

def detect_fige01(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige01.value in fig_types:
        board = fige01.fige01_detector(board, x, y)

def detect_fige02(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige02.value in fig_types:
        board = fige02.fige02_detector(board, x, y)

def detect_fige03(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige03.value in fig_types:
        board = fige03.fige03_detector(board, x, y)

def detect_fige04(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige04.value in fig_types:
        board = fige04.fige04_detector(board, x, y)

def detect_fige05(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige05.value in fig_types:
        board = fige05.fige05_detector(board, x, y)

def detect_fige06(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige06.value in fig_types:
        board = fige06.fige06_detector(board, x, y)

def detect_fige07(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fige07.value in fig_types:
        board = fige07.fige07_detector(board, x, y)

def detect_fig01(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig01.value in fig_types:
        board = fig01.fig01_detector(board, x, y)

def detect_fig02(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig02.value in fig_types:
        board = fig02.fig02_detector(board, x, y)
    
def detect_fig03(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig03.value in fig_types:
        board = fig03.fig03_detector(board, x, y)

def detect_fig04(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig04.value in fig_types:
        board = fig04.fig04_detector(board, x, y)

def detect_fig05(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig05.value in fig_types:
        board = fig05.fig05_detector(board, x, y)

def detect_fig06(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig06.value in fig_types:
        board = fig06.fig06_detector(board, x, y)

def detect_fig07(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig07.value in fig_types:
        board = fig07.fig07_detector(board, x, y)

def detect_fig08(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig08.value in fig_types:
        board = fig08.fig08_detector(board, x, y)

def detect_fig09(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig09.value in fig_types:
        board = fig09.fig09_detector(board, x, y)

def detect_fig10(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig10.value in fig_types:
        board = fig10.fig10_detector(board, x, y)

def detect_fig11(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig11.value in fig_types:
        board = fig11.fig11_detector(board, x, y)

def detect_fig12(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig12.value in fig_types:
        board = fig12.fig12_detector(board, x, y)

def detect_fig13(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig13.value in fig_types:
        board = fig13.fig13_detector(board, x, y)

def detect_fig14(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig14.value in fig_types:
        board = fig14.fig14_detector(board, x, y)

def detect_fig15(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig15.value in fig_types:
        board = fig15.fig15_detector(board, x, y)

def detect_fig16(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig16.value in fig_types:
        board = fig16.fig16_detector(board, x, y)

def detect_fig17(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig17.value in fig_types:
        board = fig17.fig17_detector(board, x, y)

def detect_fig18(board: Board, fig_types: List[str], x: int, y: int) -> Board:
    if FigType.fig18.value in fig_types:
        board = fig18.fig18_detector(board, x, y)