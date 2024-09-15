# tile_model.py

from pydantic import BaseModel, Field
from typing import Literal

class Tile(BaseModel):
    tile_color: str = Literal['red', 'yellow', 'green', 'blue']
    tile_pos_x: int = Field(..., ge=0, le=5)  
    tile_pos_y: int = Field(..., ge=0, le=5)  