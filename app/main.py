# FastApi
from uuid import uuid4
from fastapi import Cookie, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import *
# Default query parameters
from typing import Annotated, Optional

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_id")
def get_id():
    return uuid4()

# Define endline to create a new room
@app.post("/rooms/create_room",
          response_model=RoomOut,
          status_code=status.HTTP_201_CREATED)
async def create_room(new_room: RoomIn) -> RoomOut:
    if new_room.players_expected < 2 or new_room.players_expected > 4:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong amount of players")
    for room in ROOMS:
        if room["room_name"] == new_room.room_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room name already exists")
    
    try:
        last_id = ROOMS[-1]['room_id'] if ROOMS else 0
        new_id = last_id + 1

        # Create a new room dict
        roomOut = RoomOut(room_id=new_id,
                          room_name=new_room.room_name,
                          players_expected=new_room.players_expected,
                          players_names=[new_room.owner_name],
                          owner_name=new_room.owner_name,
                          is_active=True)
    
        ROOMS.append(roomOut.model_dump())
       
        return roomOut.model_dump()
    
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    