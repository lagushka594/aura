from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db import init_db
from app.sockets import sio_app

app = FastAPI(title="Aura")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.mount("/ws", sio_app)
