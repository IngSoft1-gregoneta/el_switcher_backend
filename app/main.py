# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import rooms, room_model
# Date
from datetime import datetime
# Default query parameters
from typing import Optional
app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define endline to create a new room
@app.post("/rooms/",
          response_model=room_model.RoomOut,
          status_code=status.HTTP_201_CREATED)
async def create_room(new_room: room_model.RoomIn) -> room_model.RoomOut:
    for room in rooms.ROOMS:
        if room["room_name"] == new_room.room_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room name already exists")
    try:
        last_id = rooms.ROOMS[-1]['room_id'] if rooms.ROOMS else 0
        new_id = last_id + 1

        # Create a new room dict
        room_dict = {
            "room_id": new_id,
            "room_name": new_room.room_name,
            "players_expected": new_room.players_expected,
            "players": [],
            "is_active": True,
        }

        rooms.ROOMS.append(room_dict)
        
        return room_model.RoomOut(**room_dict)
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
# Define endpoint to create a new room
@app.get("/rooms/")
async def get_rooms():
    try:
        return rooms.ROOMS
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

# endpoint for join room
@app.put("/rooms/join/")
def join_room_endpoint(room_id: int, player_name: str):
    try:
        room = rooms.get_room_by_id(room_id)

        if room is None:
            return {"message": "Room not found"}

        if len(room["players"]) == room["players_expected"]:
            return {"message": "Room is full"}
        
        if player_name in room["players"]:
            return {"message": "The name already exists, choose another"}
        
        room["players"].append(player_name)
        return {"message": f"The player {player_name} has joined the room {room_id}"}
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")