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
    is_used: bool = False
    vectors: list[tuple] = []

    def __init__(self, mov_type: MovType = None, is_used: bool = False):
        if mov_type is None:
            self.create_random_mov()
        super().__init__(mov_type=mov_type, is_used=is_used)
        self.validate_mov_type()
        self.init_vectors()

    def validate_mov_type(self):
        if self.mov_type not in MovType:
            raise ValueError(f"Tipo de movimiento invalido, {self.mov_type} no es un MovType")

    def create_random_mov(self):
        self.mov_type =  random.choice(list(MovType)).value
    
    def use_mov_card(self):
        self.is_used = True
     
    def held_mov_card(self):
        self.is_used = False

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