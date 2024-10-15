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
    vectors: list[tuple] = []

    def __init__(self, mov_type: MovType = None, mov_status: MovStatus = MovStatus.HELD, is_used: bool = False):
        if mov_type is None:
            self.create_random_mov()
        super().__init__(mov_type=mov_type, mov_status=mov_status, is_used=is_used)
        self.validate_mov_type()
        self.init_vectors()

    def validate_mov_type(self):
        if self.mov_type not in MovType:
            raise ValueError(f"Invalid mov type, {self.mov_type} is not a MovType")

    def create_random_mov(self):
        self.mov_type =  random.choice(list(MovType)).value
    
    def use_mov_card(self):
        self.is_used = True
        self.mov_status = MovStatus.PLAYED.value

    def confirm_mov_card(self):
        self.is_used = True
        self.mov_status = MovStatus.CONFIRMED.value
     
    def held_mov_card(self):
        self.is_used = False
        self.mov_status = MovStatus.HELD.value

    def init_vectors(self):
        match self.mov_type:
            case MovType.mov1:
                self.vectors = [(-2,-2),(2,-2),(-2,2),(2,2)]
            case MovType.mov2:
                self.vectors = [(-2,0),(0,-2),(2,0),(0,2)]
            case MovType.mov3:
                self.vectors = [(-1,0),(0,-1),(1,0),(0,1)]
            case MovType.mov4:
                self.vectors = [(-1,-1),(1,-1),(-1,1),(1,1)]
            case MovType.mov5:
                self.vectors = [(-2,-1),(1,-2),(2,1),(-1,2)]
            case MovType.mov6:
                self.vectors = [(-2,1),(-1,-2),(2,-1),(1,2)]
            case MovType.mov7:
                self.vectors = [(-4,0),(0,-4),(4,0),(0,4)]