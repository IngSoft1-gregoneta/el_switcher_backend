from typing import Any, List, Optional, Union
from uuid import UUID

from fastapi import HTTPException, status
from manager.manager import ConnectionManager

# from manager.manager import ConnectionManager
from models.room import RoomIn, RoomOut, RoomRepository
from starlette.status import HTTP_202_ACCEPTED

manager = ConnectionManager()


class RoomHandler:

    def __init__(self):
        self.repo = RoomRepository()

    async def get_all_rooms(self):
        return self.repo.get_rooms()

    async def get_data_from_a_room(self, room_id: UUID) -> Union[RoomOut, dict]:
        room = self.repo.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return room

    async def create_room(self, new_room: RoomIn) -> RoomOut:
        if new_room.players_expected < 2 or new_room.players_expected > 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wrong amount of players",
            )

        if self.repo.check_for_names(new_room.room_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room name already exists",
            )

        return self.repo.create_room(new_room)

    async def join_room(
        self, room_id: UUID, player_name: str, user_id: UUID, password: Optional[str]
    ) -> bool:
        room = self.repo.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if len(room.players_names) == room.players_expected:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Room is full"
            )

        if player_name in room.players_names:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Player name is already on the room, choose another name",
            )

        if room.private and not self.repo.verify_password(password, room_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bad password",
            )

        result = self.repo.update_players(
            room.players_names, player_name, room_id, "add"
        )
        return result

    async def leave_room(self, room_id: UUID, player_name: str, user_id: UUID) -> bool:
        room = self.repo.get_room_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if not (player_name in room.players_names):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        # si el owner abandona la sala, eliminar la sala
        if player_name == room.owner_name:
            result = self.repo.delete(room_id)
            return result

        result = self.repo.update_players(
            room.players_names, player_name, room_id, "remove"
        )
        return result
