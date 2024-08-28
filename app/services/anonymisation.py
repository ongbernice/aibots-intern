import re
from app.models.conversation import Conversation

def anonymize_text(text: str) -> str:
    # Basic anonymization example - replace emails with a placeholder
    anonymized_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[ANONYMIZED_EMAIL]', text)
    return anonymized_text

async def anonymize_conversation(conversation: Conversation) -> Conversation:
    for message in conversation.messages:
        message.content = anonymize_text(message.content)
    return conversation
