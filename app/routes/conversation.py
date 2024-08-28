from fastapi import APIRouter, HTTPException
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from app.services.openai_client import add_llm_response
from app.services.anonymisation import anonymize_conversation
from uuid import uuid4

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation_data: ConversationCreate):
    conversation = Conversation(
        id=str(uuid4()),
        messages=conversation_data.messages,
        user_id=conversation_data.user_id
    )
    # Anonymize the conversation before storing it
    anonymized_conversation = await anonymize_conversation(conversation)
    await anonymized_conversation.insert()
    
    # add an LLM response after creating the conversation
    conversation_with_response = await add_llm_response(anonymized_conversation.id)
    
    return conversation_with_response

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def read_conversation(conversation_id: str):
    conversation = await Conversation.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    conversation = await Conversation.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conversation.delete()
    return {"message": "Conversation deleted successfully"}

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(conversation_id: str, conversation_update: ConversationUpdate):
    conversation = await Conversation.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Update fields
    if conversation_update.user_id is not None:
        conversation.user_id = conversation_update.user_id
    if conversation_update.messages is not None:
        conversation.messages = conversation_update.messages

    # Anonymize the conversation before storing it
    anonymized_conversation = await anonymize_conversation(conversation)
    await anonymized_conversation.insert()
    
    # add an LLM response after creating the conversation
    conversation_with_response = await add_llm_response(anonymized_conversation.id)
    
    return conversation_with_response
