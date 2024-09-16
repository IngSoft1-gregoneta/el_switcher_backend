from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mov_card import MovType, MovCard

app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# lista de cartas de movimiento
mov_cards = []

# endpoint for get movements
@app.get("/matchs/{match_id}/mov_cards")
# funcion para obtener las cartas de movimiento
def get_mov_cards(match_id: int):
    # devolver una lista de cartas de movimiento que esten en la partida x
    cards = [card for card in mov_cards if card.game_id == match_id] 
    
    if not cards:
        return {"message": "Cards not found"}
      
    return [card.print_mov_card() for card in cards]


# funcion para agregar una carta de movimiento a la lista de cartas
@app.post("/matchs/{match_id}/mov_cards")
def add_mov_card(match_id: int, player_name: str, mov_type: MovType):
    if not isinstance(mov_type, MovType):
        raise HTTPException(status_code=400, detail="Invalid movement type")
        
    new_card = MovCard(match_id, player_name, mov_type)
    mov_cards.append(new_card)
    return {"message": "Card added successfully"}


    
    
    
    

