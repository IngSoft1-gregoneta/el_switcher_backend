from typing import Union
from uuid import UUID

from fastapi import HTTPException, status
from manager.manager import ConnectionManager

from models.room import RoomIn, RoomOut, RoomRepository

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
                detail="Cantidad equivocada de jugadores",
            )

        if self.repo.check_for_names(new_room.room_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nombre de sala ya en uso",
            )

        return self.repo.create_room(new_room)

    async def join_room(self, room_id: UUID, player_name: str):
        try:
            room = self.repo.get_room_by_id(room_id)
            if room is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if len(room.players_names) == room.players_expected:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Sala llena"
                )

            if player_name in room.players_names:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Jugador con dicho nombre ya existente en la sala, elija otro",
                )

            self.repo.update_players(room.players_names, player_name, room_id, "add")
            return self.repo.get_room_by_id(room_id)

        except HTTPException as http_exc:
            raise http_exc

    async def leave_room(
        self, room_id: UUID, player_name: str, user_id: UUID
    ) -> RoomOut | None:
        try:
            room = self.repo.get_room_by_id(room_id)
            if room is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if not (player_name in room.players_names):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if (
                player_name == room.owner_name
            ):  # si el owner abandona la sala, eliminar la sala
                self.repo.delete(room_id)
                return None

            self.repo.update_players(room.players_names, player_name, room_id, "remove")
            return self.repo.get_room_by_id(room_id)

        except HTTPException as http_exc:
            raise http_exc