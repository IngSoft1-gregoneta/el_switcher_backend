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
from typing import List

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define endpoint to update match state with finished turn
@app.put("/match/{room_id}/endturn/",
          response_model=room_model.RoomOut)
async def end_turn(room_id: int) -> room_model.RoomOut:
    try:
        exists = False
        # Get players list
        for room in rooms.ROOMS:
            if room["room_id"] == room_id:
                exists = True
                order: List[str] = room["players"]
                # Send to tail of list
                curr_player = order.pop(0)
                order.append(curr_player)
                room["players"] = order
    
        if not exists:
            raise HTTPException(status_code=404, detail="Room not found")

        return room
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
