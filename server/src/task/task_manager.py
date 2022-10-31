import asyncio
import time
from os import cpu_count
from concurrent.futures import ProcessPoolExecutor
from src.ws.connection_manager import ConnectionManager
from src.matrix.matrix import matrix_multiplication


class TaskManager:
    def __init__(self, connection_manager, loop, max_workers=cpu_count()):
        self.connection_manager: ConnectionManager = connection_manager
        self.loop: asyncio.AbstractEventLoop = loop
        self.executor = ProcessPoolExecutor(max_workers)

    async def add_task(self, size, task_id, start_time, timeout: float = 30.0):
        try:
            result = await asyncio.wait_for(
                self.loop.run_in_executor(
                    self.executor, matrix_multiplication, size
                ),
                timeout
            )
            await self.connection_manager.broadcast({
                "id": task_id,
                "status": "done",
                "size": size,
                "total_time": f"{time.time() - start_time:.3f}s",
                "result": result
            })
        except asyncio.exceptions.TimeoutError:
            await self.connection_manager.broadcast({
                "id": task_id,
                "status": "fail",
                "size": size,
                "total_time": f"{time.time() - start_time:.3f}s"
            })
