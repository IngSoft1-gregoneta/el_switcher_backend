from app.models.visible_match import VisibleMatchData
from models.match import * 
from figures import fige01, fige02, fige03, fige04, fige05, fige06, fige07, \
    fig01, fig02, fig03
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

def get_valid_fig_types(match: MatchOut) -> List[str]:
    fig_types: List[str] = []    
    visible_data = VisibleMatchData(match.match_id,match.players[0].player_name)
    visible_fig_cards = visible_data.me.visible_fig_cards 
    for other_player in visible_data.other_players: 
        visible_fig_cards = visible_fig_cards + other_player.visible_fig_cards
    for fig_card in visible_fig_cards:
        fig_types.append(fig_card.fig_type)
    return fig_types

# las subfiguras de otras figuras no pueden tomar fichas de la superfigura
def figures_detector(match: MatchOut):
    match_out = match
    fig_types = get_valid_fig_types(match)
    for y in range(columns):
        for x in range(columns):
            if FigType.fige01.value in fig_types and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig03.value:
                match_out = fige01.fige01_detector(match_out, x, y)
            if FigType.fige02.value in fig_types:
                match_out = fige02.fige02_detector(match_out, x, y)
            if FigType.fige03.value in fig_types and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig02.value:
                match_out = fige03.fige03_detector(match_out, x, y)
            if FigType.fige04.value in fig_types and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig01.value:
                match_out = fige04.fige04_detector(match_out, x, y)
            if FigType.fige05.value in fig_types and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig01.value and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig02.value:
                match_out = fige05.fige05_detector(match_out, x, y)
            if FigType.fige06.value in fig_types:
                match_out = fige06.fige06_detector(match_out, x, y)
            if FigType.fige07.value in fig_types and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig01.value and \
            match_out.board.tiles[coordinates_to_index(x, y)].tile_in_figure != FigType.fig03.value:
                match_out = fige07.fige07_detector(match_out, x, y)
            if FigType.fig01.value in fig_types:
                match_out = fig01.fig01_detector(match_out, x, y)
            if FigType.fig02.value in fig_types:
                match_out = fig02.fig02_detector(match_out, x, y)
            if FigType.fig03.value in fig_types:
                match_out = fig03.fig03_detector(match_out, x, y)

    match_repo.update_match(match_out)
