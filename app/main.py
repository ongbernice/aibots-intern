from fastapi import FastAPI
from app.routes.conversation import router as conversation_router
from app.db.database import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(conversation_router, prefix="/conversations", tags=["Conversations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the LLM Backend!"}
