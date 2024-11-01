from enum import Enum
from pydantic import BaseModel

# Define the Enum for card color
class CardColor(Enum):
    WHITE = "White"
    BLUE = "Blue"

    
class FigType(Enum):
    #None
    none = "None"
    # White figs (Tetris figs)
    fige01 = "fige01"
    fige02 = "fige02"
    fige03 = "fige03"
    fige04 = "fige04"
    fige05 = "fige05"
    fige06 = "fige06"
    fige07 = "fige07"
    # Blue figs (other figs)
    fig01 = "fig01"
    fig02 = "fig02"
    fig03 = "fig03"
    fig04 = "fig04"
    fig05 = "fig05"
    fig06 = "fig06"
    fig07 = "fig07"
    fig08 = "fig08"
    fig09 = "fig09"
    fig10 = "fig10"
    fig11 = "fig11"
    fig12 = "fig12"
    fig13 = "fig13"
    fig14 = "fig14"
    fig15 = "fig15"
    fig16 = "fig16"
    fig17 = "fig17"
    fig18 = "fig18"

# Define the FigCard class
class FigCard(BaseModel):
    card_color: CardColor
    fig_type: FigType
    is_visible: bool
    is_blocked: bool
    def __init__(self, card_color: CardColor, fig_type: FigType, is_visible: bool, is_blocked: bool):
        super().__init__(card_color=card_color, fig_type=fig_type, is_visible=is_visible, is_blocked=is_blocked)
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
        white_figs = list(FigType)[1:8]
        blue_figs = list(FigType)[8:]
        is_white_fig = self.fig_type in white_figs
        is_blue_fig = self.fig_type in blue_figs

        return (self.card_color == CardColor.WHITE and is_white_fig) or (self.card_color == CardColor.BLUE and is_blue_fig)
