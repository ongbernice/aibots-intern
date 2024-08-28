import os
from dotenv import load_dotenv
from openai import OpenAI

from app.models.conversation import Conversation
from app.services.anonymisation import anonymize_text
from fastapi import HTTPException

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),           
    )

async def get_llm_response(conversation: Conversation):
    messages = [{"role": msg.role, "content": msg.content} for msg in conversation.messages]
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    return response.choices[0].message.content

async def add_llm_response(conversation_id: str):
    conversation = await Conversation.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    response_content = await get_llm_response(conversation)
    # Anonymize the response before saving it
    anonymized_response_content = anonymize_text(response_content)
    conversation.messages.append({"role": "assistant", "content": anonymized_response_content})

    await conversation.save()
    return conversation
