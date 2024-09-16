from enum import Enum

# Define the Enum for card color
class CardColor(Enum):
    WHITE = "White"
    BLUE = "Blue"

# Define the Enum for white (easy) fig cards type
class FigType(Enum):
    pass

# Subclase para las figuras blancas (Tetris figs)
class FigTypeWhite(FigType):
    T = "T"
    L = "L"
    L_LEFT = "Left_L"
    I = "I"
    S = "S"
    Z = "Z"
    QUAD = "Quad"

# Subclase para las figuras azules (otras figuras)
class FigTypeBlue(FigType):
    F1 = "F1"
    Fn = "Fn"
    # Se pueden añadir más figuras azules aquí


# Define the FigCard class
class FigCard:

    def is_valid_color(self):
        return self.card_color in CardColor.__members__.values()
    
    def is_valid_fig_type(self):
        return self.fig_type in FigTypeWhite.__members__.values() or self.fig_type in FigTypeBlue.__members__.values()

    def is_valid_card(self):
        if not self.is_valid_color() or not self.is_valid_fig_type():
            return False
        else:
            is_white_fig = self.fig_type in FigTypeWhite.__members__.values()
            return (self.card_color == CardColor.WHITE and is_white_fig) or (self.card_color == CardColor.BLUE and not is_white_fig)

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
            raise ValueError(f"Invalid card color, {self.card_color} card with figure {self.fig_type} is not allowed.")
        
    def print_fig_card(self):
        print(f"id game: {self.game_id}\nplayer name: {self.player_name}\ncard color: {self.card_color}\ncard type: {self.fig_type}\nvisible card: {self.is_visible}\n")

# Example usage:
"""
try:
    # Valid card, white color and valid figure type for white cards
    card1 = FigCard(game_id=1, player_name="Player1", card_color=CardColor.WHITE, fig_type=FigTypeWhite.T)
    print(f"id game: {card1.game_id}\nplayer name: {card1.player_name}\ncard color: {card1.card_color}\ncard type: {card1.fig_type}\nvisible card: {card1.is_visible}\n")
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid card, blue color but with a figure type from white cards
    card2 = FigCard(game_id=2, player_name="Player2", card_color=CardColor.BLUE, fig_type=FigTypeWhite.L)
    print(f"id game: {card2.game_id}\nplayer name: {card2.player_name}\ncard color: {card2.card_color}\ncard type: {card2.fig_type}\nvisible card: {card2.is_visible}\n")
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid fog type
    card2 = FigCard(game_id=2, player_name="Player2", card_color=CardColor.BLUE, fig_type='y')
    print(f"id game: {card2.game_id}\nplayer name: {card2.player_name}\ncard color: {card2.card_color}\ncard type: {card2.fig_type}\nvisible card: {card2.is_visible}\n")
except ValueError as e:
    print(f"Error: {e}")

try:
    # Invalid card color
    card3 = FigCard(game_id=3, player_name="Player3", card_color='Red', fig_type=FigTypeWhite.T)
    print(f"id game: {card3.game_id}\nplayer name: {card3.player_name}\ncard color: {card3.card_color}\ncard type: {card3.fig_type}\nvisible card: {card3.is_visible}")
except ValueError as e:
    print(f"Error: {e}")
"""