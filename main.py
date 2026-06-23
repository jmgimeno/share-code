from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

connected: set[WebSocket] = set()

_static = Path(__file__).parent / "static"


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(_static / "index.html")


@app.websocket("/ws")
async def relay(websocket: WebSocket) -> None:
    await websocket.accept()
    connected.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            dead: set[WebSocket] = set()
            for peer in connected:
                try:
                    await peer.send_text(data)
                except Exception:
                    dead.add(peer)
            connected.difference_update(dead)
    except WebSocketDisconnect:
        connected.discard(websocket)
