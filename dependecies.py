from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from user import crud as user_crud
import jwt
from auth import utils

http_bearer = HTTPBearer()


def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        payload = utils.decode_jwt(token)
        
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_current_user(payload: dict = Depends(get_current_token_payload),
                     db: Session = Depends(get_db)):
    
    username = payload.get("username")

    if username is None:
        raise HTTPException(status_code=404, detail="Invalid token")
    
    user = user_crud.get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid token")
    
    return user