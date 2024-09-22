from typing import Dict
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
        # ROOM_ID USER_ID
        self.rooms: Dict[UUID | int, list[UUID | int]] = {}

    async def connect(self, user_id: UUID | int, websocket: WebSocket):
        conn = Connection(user_id, websocket)
        await websocket.accept()
        self.active_connections[user_id] = conn

    def disconnect(self, user_id: UUID | int):
        del self.active_connections[user_id]

    def bind_room(self, room_id: UUID | int, user_id: UUID | int):
        self.rooms[room_id].append(user_id)
        self.active_connections[user_id].set_playing(True)

    def unbind_room(self, room_id: UUID | int, user_id: UUID | int):
        self.rooms[room_id].remove(user_id)
        self.active_connections[user_id].set_playing(False)

    async def send_personal_message_ws(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_personal_message_id(self, user_id: UUID | int, message: str):
        await self.active_connections[user_id].get_ws().send_text(message)

    async def broadcast_by_room(self, room_id: UUID | int, message: str):
        for user_id in self.rooms[room_id]:
            await self.send_personal_message_id(user_id, message)

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
