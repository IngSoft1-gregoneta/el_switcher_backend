from enum import Enum

# Define the Enum for movement card types
class MovType(Enum):
    SIDE = "Side"
    NEXT_TO_THE_SIDE = "Next to the side"
    CROSS = "Cross"
    RIGHT_CHESS_HORSE = "Right chess horse"
    LEFT_CHESS_HORSE = "Left chess horse"

# Define the Pydantic model
class MovCard():
    def is_valid_mov_type(self):
        return self.mov_type in MovType.__members__.values()
    
    def __init__(self,game_id,player_name,mov_type):
        self.game_id: int = game_id
        self.player_name: str = player_name
        self.mov_type: MovType = mov_type
        
        if not self.is_valid_mov_type():
            raise ValueError(f"Invalid mov type, {self.mov_type} is not a MovType")
    
    def print_mov_card(self):
        print(f"id game: {self.game_id}\nplayer name: {self.player_name}\nmov type: {self.mov_type  }\n")

# Example usage:
"""
try:
    # OK
    card = MovCard(game_id=1, player_name="Player1", mov_type=MovType.SIDE)
    print(f"id game: {card.game_id}\nplayer name: {card.player_name}\nmov type: {card.mov_type.value}\n")
except ValueError as e:
    print(f"Error: {e}")
try:
    # str mov type 
    card = MovCard(game_id=1, player_name="Player1", mov_type="Side")
    print(f"id game: {card.game_id}\nplayer name: {card.player_name}\nmov type: {card.mov_type.value}")
except ValueError as e:
    print(f"Error: {e}")
"""