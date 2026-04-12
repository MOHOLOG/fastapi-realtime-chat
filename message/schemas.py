from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from user.schemas import UserResponse

class MessageCreate(BaseModel):
    text: str = Field(min_length=1)

class MessageResponse(MessageCreate):
    id: int
    user: UserResponse
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class MessageUpdate(MessageCreate):
    pass


