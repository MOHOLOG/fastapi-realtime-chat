from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=100)

    
class UserUpdate(UserCreate):
    username: str | None = Field(max_length=100, default=None)
    email: EmailStr | None = Field(max_length=50)
    password: str | None = Field(min_length=8, max_length=100, default=None)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

