# FastApi
from fastapi import FastAPI, HTTPException, status
# Middleware to allow methods from react
from fastapi.middleware.cors import CORSMiddleware
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