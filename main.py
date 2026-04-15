from contextlib import asynccontextmanager
from fastapi import FastAPI
from chat.routers import router as chat_router
from user.routers import router as user_router
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Creating database tables...")
    await init_db()
    yield 

    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(user_router)