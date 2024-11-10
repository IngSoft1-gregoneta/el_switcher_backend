import asyncio
from datetime import datetime
from typing import Dict
from uuid import UUID


async def init_timer(match_id: UUID, manager, match_handler):
    time = datetime.now()
    match_handler.timers[match_id] = time
    await manager.broadcast_by_room(match_id, str(time))
    await asyncio.sleep(120)
    if match_id in match_handler.turn_timers_task:
        del match_handler.turn_timers_task[match_id]
    print("task complete")
    await manager.broadcast_by_room(match_id, "MATCH")
    await end_turn_due_to_timer(match_id, match_handler, manager)


async def end_turn_due_to_timer(match_id: UUID, match_handler, manager):

    match = await match_handler.get_match_by_id(match_id)

    # Verifica si el player y la match existen, luego termina el turno del jugador con el turno
    if match:
        current_player = next(
            (player for player in match.players if player.has_turn), None
        )
        if current_player:
            await match_handler.end_turn(
                match_id=match_id,
                player_name=current_player.player_name,
                manager=manager,
            )


async def stop_timer(match_id: UUID, match_handler):
    if match_id in match_handler.timers:
        del match_handler.timers[match_id]
    if match_id in match_handler.turn_timers_task:
        del match_handler.turn_timers_task[match_id]


async def send_timer_message(match_id: UUID, manager, match_handler):
    if match_id in match_handler.timers:
        await manager.broadcast_by_room(match_id, str(match_handler.timers[match_id]))
