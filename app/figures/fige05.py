from app.figure_detector import *

class Fige05():
    def __init__(self):
        self.figure_detector = FigureDetector()

    def fige05_detector(self, match: MatchOut, x: int, y: int) -> MatchOut:
        match_out = match
        match_out = self.fige05_rot1_detector(match_out, x, y)
        match_out = self.fige05_rot2_detector(match_out, x, y)
        match_out = self.fige05_rot3_detector(match_out, x, y)
        match_out = self.fige05_rot4_detector(match_out, x, y)
        return match_out

    def fige05_rot1_detector(self, match: MatchOut, x: int, y: int) -> MatchOut:
        center_x = x
        center_y = y
        match_out = match
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
        if (self.fige05_rot1_verifications(center_x, center_y)):
            color = match_out.board.tiles[self.figure_detector.coordinates_to_index(x, y)].tile_color
            up = (center_x, center_y-1)
            down = (center_x, center_y+1)
            down_left = (center_x-1, center_y+1)
            if match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
                match_out.board.tiles[self.figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
        return match_out

    def fige05_rot1_verifications(self, center_x: int, center_y: int):
        return center_y-1>=0 and center_y+1<self.figure_detector.columns and center_x-1>=0

    def fige05_rot2_detector(self,match: MatchOut, x: int, y: int) -> MatchOut:
        center_x = x
        center_y = y
        match_out = match
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
        if (self.fige05_rot2_verifications(center_x, center_y)):
            color = match_out.board.tiles[self.figure_detector.coordinates_to_index(x, y)].tile_color
            up = (center_x-1, center_y)
            down = (center_x+1, center_y)
            down_left = (center_x+1, center_y+1)
            if match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
                match_out.board.tiles[self.figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
        return match_out
            
    def fige05_rot2_verifications(self, center_x: int, center_y: int):
        return center_y+1<self.figure_detector.columns and center_x-1>=0 and center_x+1<self.figure_detector.columns

    def fige05_rot3_detector(self, match: MatchOut, x: int, y: int) -> MatchOut:
        center_x = x
        center_y = y
        match_out = match
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
        if (self.fige05_rot3_verifications(center_x, center_y)):
            color = match_out.board.tiles[self.figure_detector.coordinates_to_index(x, y)].tile_color
            up = (center_x, center_y-1)
            down = (center_x, center_y+1)
            down_left = (center_x+1, center_y-1)
            if match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
                match_out.board.tiles[self.figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
        return match_out

    def fige05_rot3_verifications(self, center_x: int, center_y: int):
        return center_y-1>=0 and center_y+1<self.figure_detector.columns and center_x+1<self.figure_detector.columns

    def fige05_rot4_detector(self, match: MatchOut, x: int, y: int) -> MatchOut:
        center_x = x
        center_y = y
        match_out = match
        if match is None: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="match not found")
        if (self.fige05_rot4_verifications(center_x, center_y)):
            color = match_out.board.tiles[self.figure_detector.coordinates_to_index(x, y)].tile_color
            up = (center_x+1, center_y)
            down = (center_x-1, center_y)
            down_left = (center_x-1, center_y-1)
            if match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_color == color and \
            match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_color == color:
                match_out.board.tiles[self.figure_detector.coordinates_to_index(center_x, center_y)].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(up[0], up[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down[0], down[1])].tile_in_figure = FigType.fige05.value
                match_out.board.tiles[self.figure_detector.coordinates_to_index(down_left[0], down_left[1])].tile_in_figure = FigType.fige05.value
        return match_out
            
    def fige05_rot4_verifications(self, center_x: int, center_y: int):
        return center_y-1>=0 and center_x-1>=0 and center_x+1<self.figure_detector.columns