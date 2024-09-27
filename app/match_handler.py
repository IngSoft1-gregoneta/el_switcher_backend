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
        
    async def create_match(self, match_in: MatchIn):
        try:
            match = MatchOut(match_in.room_id)
            self.repo.create_match(match)
            return self.repo.get_match_by_id(match.match_id).model_dump(mode="json")
        except ValueError as ve:  # Capturar errores de validación específicos
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad request: {str(ve)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")
        
    async def get_match_by_id(self, match_id: int) -> Union[MatchOut, dict]:
        try:
            match = self.repo.get_match_by_id(match_id)
            if match is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return match
        
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
        