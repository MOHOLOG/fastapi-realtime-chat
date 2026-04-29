from fastapi import WebSocket
from message.schemas import MessageResponse
from collections import deque
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, dict] = dict()
    
    async def connect(self, 
                      username: str,
                      websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = {
            "websocket": websocket,
            "timestamps": deque()
        }
    
    def disconnect(self, username: str):
        del self.active_connections[username]

    async def is_rate_limited(self, username: str) -> bool:
        """
        Returns True if the user is spamming, False if they are safe to send.
        Limit: 5 messages per 10 seconds.
        """
        user_data = self.active_connections.get(username)
        if not user_data:
            return False

        timestamps = user_data["timestamps"]
        now = time.time()
        window_size = 10  
        max_messages = 5  

        while timestamps and timestamps[0] < now - window_size:
            timestamps.popleft()

        if len(timestamps) >= max_messages:
            return True

        timestamps.append(now)
        return False
    
    async def broadcast(self, 
                        username: str,
                        message: MessageResponse):
        for user, connection in self.active_connections.items():
            if user != username:
                await connection["websocket"].send_json(message.model_dump(mode="json"))