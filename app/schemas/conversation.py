from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ConversationCreate(BaseModel):
    messages: List[Message]
    user_id: str

class ConversationResponse(BaseModel):
    id: str
    messages: List[Message]
    user_id: str

class ConversationUpdate(BaseModel):
    messages: Optional[List[Message]]
    user_id: Optional[str]