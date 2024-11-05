import asyncio
from typing import Dict
from uuid import UUID

timers: Dict[UUID, int] = {}
locks: Dict[UUID, asyncio.Lock] = {}
async def init_timer(game_id: UUID,manager,match_handler):
    if game_id not in timers:
        timers[game_id] = 10
    if game_id not in locks:
        locks[game_id] = asyncio.Lock()
    timers[game_id] = 10
    while timers[game_id] > 0:
        async with locks[game_id]:  # Asegurarse de que solo una operación modifique timers[game_id]
            await manager.broadcast_by_room(game_id, f"TIMER:{str(timers[game_id])}")
            await asyncio.sleep(1)  # Espera 1 segundo sin bloquear
            timers[game_id] -= 1
    # Termino el timer
    print("task complete")
    await manager.broadcast_by_room(game_id, "MATCH")
    await end_turn_due_to_timer(game_id,match_handler,manager)


async def end_turn_due_to_timer(game_id: UUID,match_handler,manager):

    match = await match_handler.get_match_by_id(game_id)

    # Verifica si el player y la match existen, luego termina el turno del jugador con el turno
    if match:
        current_player = next((player for player in match.players if player.has_turn), None)
        if current_player:
            await match_handler.end_turn(match_id=game_id, player_name=current_player.player_name,manager = manager)

async def stop_timer(game_id: UUID):
    if game_id in timers:
        del timers[game_id]  # Elimina el temporizador del diccionario
            
#La siguiente funcion es totalmente intencionada para el fin de testear

async def set_timer(game_id: UUID, time: int):
    if game_id not in locks:
        locks[game_id] = asyncio.Lock()
    async with locks[game_id]:
        timers[game_id] = time
        
