import asyncio
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src.task.task_manager import TaskManager
from src.ws.connection_manager import ConnectionManager

app = FastAPI()

loop = asyncio.get_running_loop()
connection_manager = ConnectionManager()
task_manager = TaskManager(connection_manager, loop)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    print(f"connected: {client_id}")
    try:
        while True:
            task_size = int(await websocket.receive_text())
            start_time = time.time()
            task_id = round(start_time * 1000000 % 1000000000)

            await connection_manager.broadcast({
                "id": task_id, "status": "running", "size": task_size
            })

            asyncio.ensure_future(task_manager.add_task(task_size, task_id, start_time))
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f"disconnected: {client_id}")
