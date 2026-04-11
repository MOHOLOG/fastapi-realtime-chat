from sqlalchemy import select
from sqlalchemy.orm import Session
from user.models import User
from user.schemas import UserCreate, UserUpdate
from auth import utils

def get_user_by_username(
        username: str,
        db: Session
    ):

    return db.execute(select(User).where(User.username == username)).scalar_one_or_none()

def get_user_by_email(
        email: str,
        db: Session
    ):
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def create_user(user: UserCreate, db: Session):
    hashed_password = utils.hash_password(password=user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def update_user(current_user: User,
                new_username: str | None,
                new_email: str | None,
                new_password: str | None,
                current_password: str | None,
                db: Session):
    if new_password and current_password:
        stored_password = current_user.hashed_password.encode("utf-8")
        correct_password = utils.verify_password(passed_password=current_password.encode("utf-8"), current_password=stored_password)
        if not correct_password:
            return False
        
        current_user.hashed_password = utils.hash_password(new_password)

    else:
        raise ValueError("You should enter both new password and current password")

    if new_username:
        current_user.username = new_username

    if new_email:
        current_user.email = new_email
    
    db.commit()
    db.refresh(current_user)

    return current_user

