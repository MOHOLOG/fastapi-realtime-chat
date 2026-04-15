from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from chat.manager import ConnectionManager
from database import get_db
from user.schemas import UserCreate, UserLogin
from jwt_token.schemas import TokenResponse
from user import crud
from auth import utils

router = APIRouter()
manager = ConnectionManager()

@router.post("/register")
async def register_user(user: UserCreate,
                  db: AsyncSession = Depends(get_db)):
    
    user_email_exists = await crud.get_user_by_email(email=user.email, db=db)
    username_exists = await crud.get_user_by_username(username=user.username, db=db)
    if username_exists is not None or user_email_exists is not None:
        raise HTTPException(status_code=400, detail="Username or email address is already exists")
    
    new_user = await crud.create_user(user=user, db=db)
    
    return {
        "message": "User was created successfully",
        "username": new_user.username,
        "email": new_user.email
    }


@router.post("/login")
async def login_user(user: UserLogin,
               db: AsyncSession = Depends(get_db)):
    
    passed_password = user.password.encode("utf-8")
    stored_user = await crud.get_user_by_email(email=user.email, db=db)
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

