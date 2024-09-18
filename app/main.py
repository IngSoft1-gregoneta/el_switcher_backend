# FastApi
from fastapi import Cookie, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
# Unique id
from uuid import uuid4
# Default query parameters
from typing import Annotated
# Data from manager.py
from manager import manager
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import *

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/list_games")
def list_games():
    return [
        {"id": 1, "name": "Game 1"},
        {"id": 2, "name": "Game 2"},
        {"id": 3, "name": "Game 3"},
        {"id": 3, "name": "carade"},
    ]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# endpoint for room join request 
@app.put("/rooms/leave/")
def leave_room_endpoint(room_id: int, player_name: str):
    try:
        room = get_room_by_id(room_id)

        if room == None:
            return {"message": "Room not found"}
        if not(player_name in room["players_names"]):
            return {"message": "There is not such a player"}
        
        room["players_names"].remove(player_name)
        return {"message": f"The player {player_name} has left the room {room_id}"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
