# main.py
from fastapi import FastAPI, WebSocket
import asyncio
import json
import queue

app = FastAPI()

# Create a global task queue
task_queue = queue.Queue()

# WebSocket handling
class WebSocketQueueManager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, message: dict):
        for connection in self.connections:
            await connection.send_json(message)

queue_manager = WebSocketQueueManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await queue_manager.connect(websocket)
    try:
        while True:
            # Wait for incoming task
            task = await websocket.receive_json()

            # Add the task to the queue
            task_queue.put(task)
    except WebSocketDisconnect:
        queue_manager.connections.remove(websocket)

# Task processing
async def process_tasks():
    while True:
        if not task_queue.empty():
            task = task_queue.get()
            result = f"Processed: {task['data']}"

            # Broadcast the result to all clients
            await queue_manager.broadcast({"result": result})

            # Simulate some processing time
            await asyncio.sleep(2)

# Start task processing
loop = asyncio.get_event_loop()
loop.create_task(process_tasks())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
