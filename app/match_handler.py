from typing import Any, Union
from uuid import UUID

from fastapi import HTTPException, status

from manager.manager import ConnectionManager

#from manager.manager import ConnectionManager
from models.match import MatchIn, MatchOut, MatchRepository
    
manager = ConnectionManager()

class MatchHandler:
    def __init__(self):
        self.repo = MatchRepository()