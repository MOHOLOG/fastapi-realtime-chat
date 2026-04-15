from fastapi import WebSocket, APIRouter, Depends, status, WebSocketDisconnect
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from user import crud as user_crud
from chat import crud as chat_crud
from auth import utils
from database import get_db
from chat.manager import ConnectionManager
from message.schemas import MessageCreate, MessageResponse
from json import JSONDecodeError

manager = ConnectionManager()
router = APIRouter()

@router.websocket("/ws")
async def connect_user(websocket: WebSocket,
                       token: str,
                       db: AsyncSession = Depends(get_db)):
    try:
        user_data = utils.decode_jwt(token=token)
        username = user_data["username"]

        current_user = await user_crud.get_user_by_username(username=username, db=db)
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
            try:
                data = await websocket.receive_json()
                data = MessageCreate.model_validate(data)
                message = await chat_crud.create_message(user_id=current_user.id, message=data, db=db)
                message_response = MessageResponse.model_validate(message)

                await  manager.broadcast(username=current_user.username, message=message_response)
            
            except JSONDecodeError as e:
                print(f"Error: {e}")
                await websocket.send_text(f"Error: {e.msg}")
                continue
            
            except ValidationError as e:
                error_detail = e.errors()
                print(f"Validation error: {error_detail}")
                await websocket.send_text(f"Validation error: {error_detail[0]["msg"]}")
                continue

            await  manager.broadcast(username=username, message=message_response)
    
    except WebSocketDisconnect:
        manager.disconnect(username=current_user.username)
        print("Client disconected")