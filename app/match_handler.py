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
        
    async def create_match_modularized(self, match_in: MatchIn):
        try:
            match = MatchOut(match_in.room_id)
            self.repo.create_match(match)
            return self.repo.get_match_by_id(match_in.room_id).model_dump(mode="json")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")