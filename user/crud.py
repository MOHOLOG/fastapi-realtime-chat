from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User
from user.schemas import UserCreate, UserUpdate
from auth import utils

async def get_user_by_username(
        username: str,
        db: AsyncSession
    ):

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    return user

async def get_user_by_email(
        email: str,
        db: AsyncSession
    ):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    return user

async def create_user(user: UserCreate, db: AsyncSession):
    hashed_password = utils.hash_password(password=user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

async def update_user(current_user: User,
                new_username: str | None,
                new_email: str | None,
                new_password: str | None,
                current_password: str | None,
                db: AsyncSession):
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
    
    await db.commit()
    await db.refresh(current_user)

    return current_user

