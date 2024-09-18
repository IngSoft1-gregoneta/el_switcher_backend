from enum import Enum
from pydantic import BaseModel

# Define the Enum for card color
class CardColor(Enum):
    WHITE = "White"
    BLUE = "Blue"

class FigType(Enum):
    # White figs (Tetris figs)
    T = "T"
    L = "L"
    L_LEFT = "Left_L"
    I = "I"
    S = "S"
    Z = "Z"
    QUAD = "Quad"
    # Blue figs (other figs)
    F1 = "B1"
    # Add more blue figs as needed
    Fn = "Bn"

# Define the FigCard class
class FigCard(BaseModel):
    match_id: int
    player_name: str
    card_color: CardColor
    fig_type: FigType
    is_visible: bool = False

    def __init__(self, match_id: int, player_name: str, card_color: CardColor, fig_type: FigType):
        super().__init__(match_id=match_id, player_name=player_name, card_color=card_color, fig_type=fig_type, is_visible=False)
        self.validate_card()

    def validate_card(self):
        if not self.is_valid_color():
            raise ValueError(f"Invalid card, {self.card_color} is not a valid CardColor")
        if not self.is_valid_fig_type():
            raise ValueError(f"Invalid fig type, {self.fig_type} is not a valid FigType")
        if not self.is_valid_card():
            raise ValueError(f"Invalid card color, {self.card_color.value} card with figure {self.fig_type.value} is not allowed.")

    def is_valid_color(self):
        return self.card_color in CardColor

    def is_valid_fig_type(self):
        return self.fig_type in FigType
    
    def is_valid_card(self):
        white_figs = list(FigType)[:7]
        blue_figs = list(FigType)[7:]
        is_white_fig = self.fig_type in white_figs
        is_blue_fig = self.fig_type in blue_figs

        return (self.card_color == CardColor.WHITE and is_white_fig) or (self.card_color == CardColor.BLUE and is_blue_fig)
