# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
# data, methods and classes of a room
from room import rooms
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

# endpoint for room join request 
@app.put("/rooms/randomize/")
def sort_players_randomly_endpoint(room_id: int):
    try:
        
        room = rooms.get_room_by_id(room_id)
        

        if room == None:    
            return {"message": "Room not found"}
        
        
        rooms.sort_players(room)
        return {"message": "Players sorted succesfuly"}
        

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

