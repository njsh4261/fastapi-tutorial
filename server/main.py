import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.task.task_manager import TaskManager
from src.ws.connection_manager import ConnectionManager

app = FastAPI()

connection_manager = ConnectionManager()
task_manager = TaskManager(connection_manager, asyncio.get_running_loop())


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    print(f"connected: {client_id}")
    try:
        while True:
            task_size = int(await websocket.receive_text())
            asyncio.ensure_future(task_manager.add_task(task_size))
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f"disconnected: {client_id}")
