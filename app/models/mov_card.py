from pydantic import BaseModel, validator
from enum import Enum
import random

# Define the Enum for movement card types
class MovType(Enum):
    SIDE = "Side"
    NEXT_TO_THE_SIDE = "Next to the side"
    CROSS = "Cross"
    RIGHT_CHESS_HORSE = "Right chess horse"
    LEFT_CHESS_HORSE = "Left chess horse"

    
# Define the Pydantic model
class MovCard(BaseModel):
    match_id: int
    player_name: str
    mov_type: MovType

    def __init__(self, *, match_id: int, player_name: str, mov_type: MovType = None):
        if mov_type is None:
            mov_type = self.create_random_mov()
        # Initialize the BaseModel with the given parameters
        super().__init__(match_id=match_id, player_name=player_name, mov_type=mov_type)
        self.validate_mov_type()

    def validate_mov_type(self):
        if self.mov_type not in MovType:
            raise ValueError(f"Invalid mov type, {self.mov_type} is not a MovType")

    def create_random_mov(self) -> MovType:
        return random.choice(list(MovType))
