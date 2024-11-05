from fastapi.testclient import TestClient
from fastapi import status
from main import app, manager,match_handler
from models.match import *
from models.room import * 
from models.timer import *

repo_room = RoomRepository()
repo_match = MatchRepository()

client = TestClient(app)
    
room_id = uuid1()

def reset():
    repo_room.delete_rooms()
    repo_match.delete_matchs()

def generate_test_room():
    db = Session()
    try:
        roombd1 = Room(
                room_name="Room 1",
                room_id=str(room_id),
                players_expected=2,
                owner_name="Braian",
                players_names=json.dumps(["Braian","Tadeo"]),
                is_active=True
            )
        db.add(roombd1)
        db.commit()
    finally:
        db.close()    

async def generate_test_match():
    try:
        await match_handler.create_match(room_id,"Braian",manager)
    except:
        assert False, f"Creando mal matchs en db"

def get_match(room_id):
    match = repo_match.get_match_by_id(room_id)
    return match
        
async def test_timer():
    # Resetea la base de datos antes de iniciar el test
    reset()
    
    # Genera la sala y partida de prueba
    generate_test_room()
    await generate_test_match()
    
    # Configura el temporizador y llama a init_timer
    await set_timer(room_id,1)
    # Espera a que el temporizador termine
    await asyncio.sleep(1.5)  # Tiempo suficiente para que el temporizador llegue a 0
    
    match = await match_handler.get_match_by_id(room_id)
    # Verifica el estado del turno después de que el temporizador llegue a 0
    assert not match.players[0].has_turn, "El turno no cambió correctamente después de que el temporizador llegó a cero"
    assert match.players[1].has_turn, "El turno debería haber pasado al siguiente jugador"
    
    # Detiene el temporizador por si aún queda alguna tarea activa

# Ejecuta el test
asyncio.run(test_timer())