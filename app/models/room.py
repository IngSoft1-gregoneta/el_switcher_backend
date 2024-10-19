import json
from typing import List
from uuid import UUID, uuid1

from config.repositorymanager import Room, Session
from pydantic import BaseModel


class RoomIn(BaseModel):
    room_name: str
    players_expected: int
    owner_name: str


class RoomOut(BaseModel):
    room_id: UUID
    room_name: str
    players_expected: int
    players_names: List[str] = []
    owner_name: str
    is_active: bool = True


class RoomRepository:
    def create_room(self, new_room: RoomIn):
        db = Session()
        try:
            new_id = uuid1()

            roomOut = RoomOut(
                room_id=new_id,
                room_name=new_room.room_name,
                players_expected=new_room.players_expected,
                players_names=[new_room.owner_name],
                owner_name=new_room.owner_name,
                is_active=True,
            )

            roombd = Room(
                room_name=new_room.room_name,
                room_id=str(new_id),
                players_expected=new_room.players_expected,
                owner_name=new_room.owner_name,
                players_names=json.dumps(roomOut.players_names),
                is_active=True,
            )
            db.add(roombd)
            db.commit()
            return roomOut.model_dump()
        finally:
            db.close()

    # Extrae sala por id o devuelve None si no encuentra la sala
    def get_room_by_id(self, room_id: UUID) -> RoomOut | None:
        db = Session()
        try:
            result = db.query(Room).filter(Room.room_id == str(room_id)).one_or_none()
            if result:
                room = RoomOut(
                    room_id=result.room_id,
                    room_name=result.room_name,
                    players_expected=result.players_expected,
                    players_names=json.loads(result.players_names) or [],
                    owner_name=result.owner_name,
                    is_active=result.is_active,
                )
                return room
            return None
        finally:
            db.close()

    # Metodos posibles: add, remove
    def update_players(
        self, players: List[str], player_name: str, room_id: UUID, method: str
    ):
        if method == "add":
            players.append(player_name)
        elif method == "remove" and player_name in players:
            players.remove(player_name)

        db = Session()
        try:
            db_room = db.query(Room).filter(Room.room_id == str(room_id)).one()
            db_room.players_names = json.dumps(players)
            db.commit()
        finally:
            db.close()

    def get_rooms(self):
        db = Session()
        try:
            rooms = db.query(Room).all()
            rooms_out = []
            for room in rooms:
                rooms_out.append(RoomOut(
                    room_id=room.room_id,
                    room_name=room.room_name,
                    players_expected=room.players_expected,
                    players_names=json.loads(room.players_names) or [],
                    owner_name=room.owner_name,
                    is_active=room.is_active,
                ).model_dump())
            return rooms_out
        finally:
            db.close()

    def check_for_names(self, room_name: str):
        db = Session()
        try:
            return db.query(Room).filter(Room.room_name == room_name).first()
        finally:
            db.close()

    def delete(self, room_id: UUID):
        db = Session()

        try:
            todelete = db.query(Room).filter(Room.room_id == str(room_id)).one_or_none()
            db.delete(todelete)
            db.commit()
        finally:
            db.close()

    def delete_rooms(self):
        db = Session()
        try:
            db.query(Room).delete()
            db.commit()
        finally:
            db.close()