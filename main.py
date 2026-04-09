from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets import broadcast
from manager import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def connect_user(username: str,
                       websocket: WebSocket):
    await manager.connect(username=username, websocket=websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await  manager.broadcast(data)
    
    except WebSocketDisconnect:
        manager.disconnect(username=username)
        print("Client disconected")