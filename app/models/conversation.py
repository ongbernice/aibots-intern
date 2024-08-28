from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class Conversation(Document):
    id: PydanticObjectId = None
    messages: List[Message]
    user_id: str

    class Settings:
        collection = "conversations"