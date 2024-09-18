# FastApi
from uuid import uuid4
from fastapi import Cookie, FastAPI, WebSocket, WebSocketDisconnect
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# Default query parameters
from typing import Annotated
# Data from manager.py
from manager import manager

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = manager.ConnectionManager()
# Aca podriamos asignar el mismo socket para el grupo de jugadores en la misma partida?
user_socket = {}

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user_id: Annotated[str | None, Cookie()] = None
):
   # logger.debug(user_id)
    await manager.connect(websocket)
    user_socket[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
@app.get("/get_id")
def get_id():
    return uuid4()

