import json
from typing import Dict, Union, List
from uuid import UUID

from fastapi import WebSocket, WebSocketDisconnect


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[Union[UUID, int], WebSocket] = {}

    async def send_chat_message(self, sender_id: Union[UUID, int], message: str):
        for user, user_ws in self.active_connections.items():
            await user_ws.send_text(json.dumps({
                "user_id": str(sender_id),
                "content": message
            }))

    async def add_connection(self, user_id: Union[UUID, int], websocket: WebSocket):
        self.active_connections[user_id] = websocket

    async def disconnect_chat(self, user_id: Union[UUID, int]):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_log_event(self, event_type: str, message: str):
        for user_ws in self.active_connections.values():
            await user_ws.send_text(json.dumps({
                "event_type": event_type,
                "content": message
                }))



