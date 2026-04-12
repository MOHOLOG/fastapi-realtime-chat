from sqlalchemy import select
from sqlalchemy.orm import Session
from message.models import Message
from message.schemas import MessageCreate
from user.crud import get_user_by_username
from user.models import User


def create_message(user_id: int, 
                   message: MessageCreate,
                   db: Session):

    new_message = Message(
        text = message.text,
        user_id = user_id,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message