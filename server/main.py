import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.task.task_manager import TaskManager
from src.ws.connection_manager import ConnectionManager

app = FastAPI()

connection_manager = ConnectionManager()
task_manager = TaskManager(connection_manager, asyncio.get_running_loop())


def parse(message):
    to_dict: dict = json.loads(message)

    size = 0
    try:
        size = int(to_dict["work_size"])
    except ValueError:
        pass

    timeout = 30.0
    try:
        timeout = float(to_dict["timeout"])
    except ValueError:
        pass

    return size, timeout


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    print(f"connected: {client_id}")
    try:
        while True:
            asyncio.ensure_future(
                task_manager.add_task(*parse(await websocket.receive_text()))
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f"disconnected: {client_id}")
