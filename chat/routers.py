from fastapi import WebSocket, APIRouter, Depends, status, WebSocketDisconnect
from sqlalchemy.orm import Session
import jwt
from user import crud
from auth import utils
from database import get_db
from chat.manager import ConnectionManager

manager = ConnectionManager()
router = APIRouter()

@router.websocket("/ws")
async def connect_user(websocket: WebSocket,
                       token: str,
                       db: Session = Depends(get_db)):
    try:
        user_data = utils.decode_jwt(token)
        username = user_data["username"]

        current_user = crud.get_user_by_username(username=username, db=db)
        if not current_user:
            print("BOUNCER: User not found in database!")
            raise ValueError("User not found")
        
    except jwt.ExpiredSignatureError:
        print("BOUNCER: Token is expired!")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    except (jwt.PyJWTError, ValueError) as e:
        print(f"BOUNCER: Invalid token or error - {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    print(f"BOUNCER: Letting {username} into the room!")
    await manager.connect(username=username, websocket=websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await  manager.broadcast(data)
    
    except WebSocketDisconnect:
        manager.disconnect(username=current_user.username)
        print("Client disconected")