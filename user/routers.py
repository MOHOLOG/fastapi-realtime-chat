from fastapi import HTTPException, WebSocket, WebSocketDisconnect, APIRouter, Depends, status
from sqlalchemy.orm import Session
from dependecies import get_current_user
from chat.manager import ConnectionManager
from database import get_db
from user.schemas import UserCreate, UserLogin
from user.models import User
from jwt_token.schemas import TokenResponse
from user import crud
from auth import utils
import jwt

router = APIRouter()
manager = ConnectionManager()

@router.post("/register")
def register_user(user: UserCreate,
                  db: Session = Depends(get_db)):
    
    user_exists = crud.get_user_by_email(email=user.email, db=db)
    if user_exists is not None:
        raise HTTPException(status_code=401, detail="This email is already taken")
    
    new_user = crud.create_user(user=user, db=db)
    
    return {
        "message": "User was created successfully",
        "username": new_user.username,
        "email": new_user.email
    }


@router.post("/login")
def login_user(user: UserLogin,
               db: Session = Depends(get_db)):
    
    passed_password = user.password.encode("utf-8")
    stored_user = crud.get_user_by_email(email=user.email, db=db)
    if stored_user:
        stored_password = stored_user.hashed_password.encode("utf-8")
        if utils.verify_password(passed_password=passed_password, current_password=stored_password):
            jwt_payload = {
                "username": stored_user.username,
                "email": stored_user.email
            }
            token = utils.encode_jwt(jwt_payload)
            return TokenResponse(secret_token=token, token_type="bearer")

        else:
            raise HTTPException(status_code=404, detail="Invalid password or email")
    
    else:
        raise HTTPException(status_code=404, detail="Invalid password or email")

