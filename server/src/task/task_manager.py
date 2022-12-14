import asyncio
import time
from multiprocessing import Process, Manager

from src.matrix.matrix import matrix_multiplication
from src.ws.connection_manager import ConnectionManager


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
        self.manager = Manager()

    async def add_task(self, task_size, task_timeout):
        start_time = time.time()
        task_id = round(start_time * 1000000 % 1000000000)

        task_status = {
            "id": task_id, "status": "running", "size": task_size,
            "timeout": f"{task_timeout}s"
        }
        await self.connection_manager.broadcast(task_status)
        try:
            result = self.manager.dict()
            await asyncio.wait_for(
                self.loop.run_in_executor(
                    None, run_task, matrix_multiplication, task_timeout, task_size, result
                ),
                None
            )
            task_status["status"] = "done"
            task_status["result"] = dict(result)
        except asyncio.exceptions.TimeoutError:
            task_status["status"] = "fail"
        finally:
            task_status["total_time"] = f"{time.time() - start_time:.3f}s"
            await self.connection_manager.broadcast(task_status)
