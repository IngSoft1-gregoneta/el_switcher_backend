from enum import Enum

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
    F1 = "F1"
    """...""" # Add blue figs here
    Fn = "Fn"


# Define the FigCard class
class FigCard:

    def is_valid_color(self):
        return self.card_color in CardColor.__members__.values()
    
    def is_valid_fig_type(self):
        return self.fig_type in FigType.__members__.values() 
    
    def is_valid_card(self):
        if not self.is_valid_color() or not self.is_valid_fig_type():
            return False
        else:
            white_figs = list(FigType)[:7]
            blue_figs = list(FigType)[7:] 
            is_white_fig = self.fig_type in white_figs
            is_blue_fig = self.fig_type in blue_figs 

            return (self.card_color == CardColor.WHITE and is_white_fig) or (self.card_color == CardColor.BLUE and is_blue_fig)

    def __init__(self, game_id, player_name, card_color, fig_type):
        self.game_id: int = game_id
        self.player_name: str = player_name
        self.card_color: CardColor = card_color  # White or blue card
        self.fig_type: FigType = fig_type  # Will hold the figure type, either white or blue
        self.is_visible: bool = False  # True if card in use, False if card in the deck
        
        # Validate card before creating it
        if not self.is_valid_color():
            raise ValueError(f"Invalid card, {self.card_color} is not a CardColor")
        if not self.is_valid_fig_type():
            raise ValueError(f"Invalid fig type, {self.fig_type} is not a FigType")
        if not self.is_valid_card():
            raise ValueError(f"Invalid card color, {self.card_color.value} card with figure {self.fig_type.value} is not allowed.")
        
    def print_fig_card(self):
        print(f"id game: {self.game_id}\nplayer name: {self.player_name}\ncard color: {self.card_color.value}\ncard type: {self.fig_type.value}\nvisible card: {self.is_visible}\n")

# Example usage:
"""
try:
    # Valid card, white color and valid figure type for white cards
    card1 = FigCard(game_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=FigType.T)
    card1.print_fig_card()
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid card, blue color but with a figure type from white cards
    card2 = FigCard(game_id=2, player_name="Player2", card_color=CardColor.BLUE, fig_type=FigType.L)
    card2.print_fig_card()
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid fog type
    card3 = FigCard(game_id=2, player_name="Player2", card_color=CardColor.BLUE, fig_type='y')
    card3.print_fig_card()
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid card color
    card4 = FigCard(game_id=3, player_name="Player3", card_color='Red', fig_type=FigType.T)
    card4.print_fig_card()
except ValueError as e:
    print(f"Error: {e}")
"""