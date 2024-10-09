from pydantic import BaseModel, validator
from enum import Enum
import random

# Define the Enum for movement card types
class MovType(Enum):
    mov1 = "mov1"
    mov2 = "mov2"
    mov3 = "mov3"
    mov4 = "mov4"
    mov5 = "mov5"
    mov6 = "mov6"
    mov7 = "mov7"

class MovStatus(Enum):
    HELD = 'Held'
    PLAYED = 'Played'
    CONFIRMED = 'Confirmed'
    
# Define the Pydantic model
class MovCard(BaseModel):
    mov_type: MovType
    mov_status: MovStatus = MovStatus.HELD
    is_used: bool = False

    def __init__(self, mov_type: MovType = None, mov_status: MovStatus = MovStatus.HELD, is_used: bool = False):
        if mov_type is None:
            mov_type = self.create_random_mov()
        super().__init__(mov_type=mov_type, mov_status=mov_status, is_used=is_used)
        self.validate_mov_type()

    def validate_mov_type(self):
        if self.mov_type not in MovType:
            raise ValueError(f"Invalid mov type, {self.mov_type} is not a MovType")

    def create_random_mov(self) -> MovType:
        return random.choice(list(MovType))
    
    def use_mov_card(self):
        self.is_used = True
        self.mov_status = MovStatus.PLAYED

    def confirm_mov_card(self):
        self.is_used = True
        self.mov_status = MovStatus.CONFIRMED
     
    def held_mov_card(self):
        self.is_used = False
        self.mov_status = MovStatus.HELD 
