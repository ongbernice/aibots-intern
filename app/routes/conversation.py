from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate
from app.services.openai_client import add_llm_response
from app.services.anonymisation import anonymize_conversation

router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation_data: ConversationCreate) -> Conversation:
    conversation = Conversation(
        **conversation_data.dict()
    )
    # Anonymize the conversation before storing it
    anonymized_conversation = await anonymize_conversation(conversation)
    await anonymized_conversation.insert()
    
    # add an LLM response after creating the conversation
    conversation_with_response = await add_llm_response(anonymized_conversation.id)
    
    return conversation_with_response

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def read_conversation(conversation_id: str):
    conversation_id_obj = PydanticObjectId(conversation_id)
    conversation = await Conversation.get(conversation_id_obj)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    conversation_id_obj = PydanticObjectId(conversation_id)
    conversation = await Conversation.get(conversation_id_obj)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await conversation.delete()
    return {"message": "Conversation deleted successfully"}

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(conversation_id: str, conversation_data: ConversationUpdate) -> Conversation:
    conversation_id_obj = PydanticObjectId(conversation_id)
    conversation = await Conversation.get(conversation_id_obj)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    update_data = conversation_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)

    # Anonymize the conversation before storing it
    anonymized_conversation = await anonymize_conversation(conversation)
    await anonymized_conversation.save()
    
    # add an LLM response after creating the conversation
    conversation_with_response = await add_llm_response(anonymized_conversation.id)
    
    return conversation_with_response
