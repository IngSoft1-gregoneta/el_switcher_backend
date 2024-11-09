import asyncio
from typing import Dict
from uuid import UUID

timers: Dict[UUID, int] = {}
locks: Dict[UUID, asyncio.Lock] = {}
async def init_timer(match_id: UUID,time:int,manager,match_handler):
    if match_id not in timers:
        timers[match_id] = time
    if match_id not in locks:
        locks[match_id] = asyncio.Lock()
    timers[match_id] = time
    await manager.broadcast_by_room(match_id, f"TIMER: STARTS {str(timers[match_id])}")
    while timers[match_id] > 0:
        async with locks[match_id]:
            await asyncio.sleep(1)
            timers[match_id] -= 1
    # Termino el timer
    print("task complete")
    await manager.broadcast_by_room(match_id, f"TIMER: FINISHED")
    await manager.broadcast_by_room(match_id, "MATCH")
    await end_turn_due_to_timer(match_id,match_handler,manager)


async def end_turn_due_to_timer(match_id: UUID,match_handler,manager):

    match = await match_handler.get_match_by_id(match_id)

    # Verifica si el player y la match existen, luego termina el turno del jugador con el turno
    if match:
        current_player = next((player for player in match.players if player.has_turn), None)
        if current_player:
            await match_handler.end_turn(match_id=match_id, player_name=current_player.player_name,manager = manager)

async def stop_timer(match_id: UUID):
    if match_id in timers:
        del timers[match_id]  # Elimina el temporizador del diccionario
            
