import asyncio
import time
from multiprocessing import Process
from src.ws.connection_manager import ConnectionManager
from src.matrix.matrix import matrix_multiplication


def run_task(func, timeout, *args, **kwargs):
    process = Process(target=func, args=args, kwargs=kwargs)
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        raise asyncio.exceptions.TimeoutError()


class TaskManager:
    def __init__(self, connection_manager, loop):
        self.connection_manager: ConnectionManager = connection_manager
        self.loop: asyncio.AbstractEventLoop = loop

    async def add_task(self, size, task_id, start_time, timeout: float = 30.0):
        try:
            result = await asyncio.wait_for(
                self.loop.run_in_executor(
                    None, run_task, matrix_multiplication, timeout, size
                ),
                None
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
