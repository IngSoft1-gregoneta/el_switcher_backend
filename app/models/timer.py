from typing import Dict
import asyncio
from uuid import UUID
from ..main import manager
from ..match_handler import MatchHandler

timers: Dict[UUID, int] = {}
async def init_timer(game_id: UUID):
    if game_id not in timers:
        timers[game_id] = 120
    while timers[game_id] > 0:
        manager.broadcast_by_room(game_id, f"TIMER:{str(timers[game_id])}")
        await asyncio.sleep(1)  # Espera 1 segundo sin bloquear
        timers[game_id] -= 1
    # Termino el timer
    await end_turn_due_to_timer(game_id)

async def reset_timer(game_id: UUID):
    if game_id in timers:
        timers[game_id] = 120
    
async def end_turn_due_to_timer(game_id: UUID):
    match_handler = MatchHandler()
    match = await match_handler.get_match_by_id(game_id)

    # Verifica si el partido existe y si hay un jugador con turno actual
    if match:
        current_player = next((player for player in match.players if player.has_turn), None)
        if current_player:
            await match_handler.end_turn(match_id=game_id, player_name=current_player.name)
        
