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
"""
curl -X POST "http://localhost:8000/rooms/" -H "accept: application/json" -H "Content-Type: application/json" -w "\n" -i -d "{\"room_name\":\"Room2\",\"players_expected\":2}"

"""

