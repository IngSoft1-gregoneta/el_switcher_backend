from pydantic import BaseModel, Field
from typing import List

class RoomIn(BaseModel):
    room_name: str = Field(..., min_length=1, max_length=50)
    players_expected: int = Field(..., ge=2, le=4)  # between 2 and 4

class RoomOut(BaseModel):
    room_id: int
    room_name: str
    players_expected: int
    players: List[str] = []
    is_active: bool