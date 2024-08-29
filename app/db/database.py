import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.conversation import Conversation

# Fetch MongoDB URI from environment variables
MONGODB_URI = os.getenv("DATABASE_URL", "mongodb://mongodb:27017/mydatabase")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Access the database
db = client.get_default_database()

# Initialize Beanie ODM with the models
async def init_db():
    await init_beanie(database=db, document_models=[Conversation])
