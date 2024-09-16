import logging
from typing import Annotated, Union
from uuid import UUID, uuid1, uuid4

from fastapi import Cookie, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


app = FastAPI()

origins = ["http://localhost:5173", "localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        logger.debug("BROADCASTE///////////////////")
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


manager = ConnectionManager()
# Aca podriamos asignar el mismo socket para el grupo de jugadores en la misma partida?
user_socket = {}


# TODO: Borrar en merge y poner el que va
class Game(BaseModel):
    id: UUID
    name: str


games = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_id")
def get_id():
    return uuid4()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, user_id: Annotated[str | None, Cookie()] = None
):
    logger.debug(user_id)
    await manager.connect(websocket)
    user_socket[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# TODO: Dejar la api correcta
@app.get("/list_games")
def list_games():
    return games


# TODO: Mandar broadcast con un id que signifique que se agregaron partidas
# TODO: Borrar esto
# esto es de ejemplo para probar websockets
@app.post("/add_game/")
async def add_game(game: Game):
    games.append(game)
    await manager.broadcast("Game created")
    # await manager.send_personal_message("Game created", user_socket[0])
    return 200


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
