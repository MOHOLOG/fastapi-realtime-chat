from fastapi import FastAPI
from chat.routers import router as chat_router
from user.routers import router as user_router
from database import init_db

init_db()

app = FastAPI()

app.include_router(chat_router)
app.include_router(user_router)