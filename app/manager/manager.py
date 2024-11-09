from typing import Dict, Union
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect


class Connection:
    def __init__(self, user_id: UUID | int, ws: WebSocket):
        self.user_id = user_id
        self.ws = ws
        self.is_playing = False

    def set_playing(self, is_playing: bool):
        self.is_playing = is_playing

    def get_ws(self):
        return self.ws


class ConnectionManager:
    def __init__(self):
        # USER_ID
        self.active_connections: Dict[UUID | int, Connection] = {}
        # ROOM_ID list(USER_ID)
        self.rooms: Dict[UUID | int, list[UUID]] = {}

    async def connect(self, user_id: UUID | int, websocket: WebSocket):
        conn = Connection(user_id, websocket)
        await websocket.accept()
        self.active_connections[user_id] = conn
        # print("CONN ", self.active_connections)

    def disconnect(self, user_id: UUID | int):
        # TODO: think another way  this should be sooo slow
        # TODO: also we could think if we should reconnect, maybe we shouldnt remove from the list
        # TODO: what happens if we try to send a message where there is no connection?
        # for _, list_uuid in self.rooms.items():
        #     if user_id in list_uuid:
        #         list_uuid.remove(user_id)
        del self.active_connections[user_id]

    def bind_room(self, room_id: UUID | int, user_id: UUID):
        self.rooms.setdefault(room_id, [])
        self.rooms[room_id].append(user_id)
        self.active_connections[user_id].set_playing(True)

    def unbind_room(self, room_id: UUID | int, user_id: UUID):
        self.rooms[room_id].remove(user_id)
        self.active_connections[user_id].set_playing(False)

    async def send_personal_message_ws(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_message_id(self, user_id: UUID | int, message: str):
        try:
            await self.active_connections[user_id].get_ws().send_text(message)
        except Exception as e:
            return 

    async def broadcast_by_room(self, room_id: UUID | int, message: str):
        for user_id in self.rooms[room_id]:
            # print(user_id, " ", message)
            try:
                # If ws of user_id disconnect we shoulnt send a message
                await self.send_personal_message_id(user_id, message)
            except Exception as e:
                return

    async def broadcast_not_playing(self, message: str):
        for uuid, connection in self.active_connections.items():
            try:
                if not connection.is_playing:
                    await connection.get_ws().send_text(message)
            except WebSocketDisconnect:
                self.disconnect(uuid)

    async def broadcast(self, message: str):
        for uuid, connection in self.active_connections.items():
            try:
                await connection.get_ws().send_text(message)
            except WebSocketDisconnect:
                self.disconnect(uuid)

    async def join(self, room_id: UUID | int, user_id: UUID):
        try:
            self.bind_room(room_id, user_id)
            await self.broadcast_not_playing("LISTA")
            await self.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            return

    async def leave(self, room_id: UUID | int, user_id: UUID):
        # TODO: Mock WS asi no usamos trry, o mas bien los usamos para reconectar
        try:
            self.unbind_room(room_id, user_id)
            await self.broadcast_not_playing("LISTA")
            await self.broadcast_by_room(room_id, "ROOM")
        except Exception as e:
            return  # Esto es para propositos de evitar el error:1

    async def leave_match(self, room_id: UUID | int, user_id: UUID):
        # TODO: Mock WS asi no usamos trry, o mas bien los usamos para reconectar
        try:
            self.unbind_room(room_id, user_id)
            await self.broadcast_not_playing("LISTA")
            await self.broadcast_by_room(room_id, "MATCH")
        except Exception as e:
            return

    async def create(self, room_id: UUID | int, user_id: UUID):
        try:
            self.bind_room(room_id, user_id)
            await self.broadcast_not_playing("LISTA")
        except Exception as e:
            raise Exception(f"Error:{str(e)}")

    async def destroy_room(self, room_id: UUID | int):
        try:
            await self.broadcast_by_room(room_id, "ROOM")
            for userid in list(self.rooms[room_id]):
                self.unbind_room(room_id, userid)
            await self.broadcast_not_playing("LISTA")
            del self.rooms[room_id]
        except Exception as e:
            raise Exception(f"Error:{str(e)}")
