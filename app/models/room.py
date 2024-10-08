import json
from typing import List
from uuid import UUID, uuid1

from pydantic import BaseModel, Field


class RoomIn(BaseModel):
    room_name: str
    players_expected: int
    owner_name: str


class RoomOut(BaseModel):
    room_id: UUID
    room_name: str
    players_expected: int
    players_names: List[str] = []
    players_UUIDs: List[UUID] = []
    owner_name: str
    is_active: bool = True


