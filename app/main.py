from typing import Union

from fastapi import FastAPI, HTTPException, status
from room import rooms
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define endpoint to create a new room
@app.get("/rooms/")
async def get_rooms():
    try:
        return rooms.ROOMS
    except Exception as e:
        print(f"Error: {e}")  # Debug error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
