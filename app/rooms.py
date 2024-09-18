from pydantic import BaseModel, Field 
from typing import List

class RoomIn(BaseModel):
    room_name: str
    players_expected: int
    owner_name: str

class RoomOut(BaseModel):
    room_id: int
    room_name: str
    players_expected: int
    players_names: List[str] = []
    owner_name: str
    is_active: bool = True
# Rooms list
ROOMS = [
]

# Fetch room by id or return None if the room was not found
def get_room_by_id(room_id: int):
    for room in ROOMS:
        if room["room_id"] == room_id:
            return room
    return None