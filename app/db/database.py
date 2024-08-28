import motor.motor_asyncio
from beanie import init_beanie
from app.models.conversation import Conversation

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.my_database, document_models=[Conversation])