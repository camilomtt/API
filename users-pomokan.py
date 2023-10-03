from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Datos de prueba
users = []
boards = []
cards = []


class User(BaseModel):
    name: str
    email: str
    password: str


class Board(BaseModel):
    name: str


class Card(BaseModel):
    title: str
    description: str


@app.post("/signup")
async def signup(user: User):
    users.append(user)
    return {"message": "Usuario registrado con éxito"}


@app.post("/login")
async def login(user: User):
    for u in users:
        if u.email == user.email and u.password == user.password:
            return {"message": "Inicio de sesión exitoso"}
    return {"message": "Credenciales incorrectas"}


@app.get("/boards")
async def get_boards():
    return boards


@app.post("/boards/create")
async def create_board(board: Board):
    boards.append(board)
    return {"message": "Tablero creado"}


@app.get("/boards/{board_id}/cards")
async def get_cards(board_id: int):
    if board_id < len(boards):
        return cards
    return {"message": "Tablero no encontrado"}


@app.post("/boards/{board_id}/cards/create")
async def create_card(board_id: int, card: Card):
    if board_id < len(boards):
        cards.append(card)
        return {"message": "Tarjeta creada en el tablero"}
    return {"message": "Tablero no encontrado"}
