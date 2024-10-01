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
    
# Define the Pydantic model
class MovCard(BaseModel):
    mov_type: MovType

    def __init__(self, mov_type: MovType = None):
        if mov_type is None:
            mov_type = self.create_random_mov()
        super().__init__(mov_type=mov_type)
        self.validate_mov_type()

    def validate_mov_type(self):
        if self.mov_type not in MovType:
            raise ValueError(f"Invalid mov type, {self.mov_type} is not a MovType")

    def create_random_mov(self) -> MovType:
        return random.choice(list(MovType))
