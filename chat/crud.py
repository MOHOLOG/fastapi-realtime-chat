from sqlalchemy.ext.asyncio import AsyncSession
from message.models import Message
from message.schemas import MessageCreate

async def create_message(user_id: int, 
                   message: MessageCreate,
                   db: AsyncSession):

    new_message = Message(
        text = message.text,
        user_id = user_id,
    )

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return new_message