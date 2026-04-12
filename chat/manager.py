from fastapi import WebSocket
from user.models import User
from message.models import Message
from message.schemas import MessageResponse
from user.schemas import UserResponse

class ConnectionManager:
    def __init__(self):
        self.active_connections = dict()
    
    async def connect(self, 
                      username: str,
                      websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
    
    def disconnect(self, username: str):
        del self.active_connections[username]
    
    async def broadcast(self, message: MessageResponse):
        for connection in self.active_connections.values():
            await connection.send_json(message.model_dump(mode="json"))