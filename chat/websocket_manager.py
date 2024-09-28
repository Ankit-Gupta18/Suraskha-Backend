from typing import Dict
from fastapi import WebSocket
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.lock = asyncio.Lock()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections[user_id] = websocket
            print(f"User {user_id} connected.")

    def disconnect(self, user_id: int):
        async def _disconnect():
            async with self.lock:
                if user_id in self.active_connections:
                    del self.active_connections[user_id]
                    print(f"User {user_id} disconnected.")
        asyncio.create_task(_disconnect())

    async def send_personal_message(self, message: str, user_id: int):
        async with self.lock:
            websocket = self.active_connections.get(user_id)
            if websocket:
                await websocket.send_text(message)

    async def broadcast(self, message: str):
        async with self.lock:
            for connection in self.active_connections.values():
                await connection.send_text(message)
