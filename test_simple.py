import asyncio
from beanie import PydanticObjectId

from app.routes.conversation import create_conversation, read_conversation, update_conversation, delete_conversation
from app.schemas.conversation import ConversationCreate, ConversationUpdate
from app.models.conversation import Conversation
from app.db.database import init_db

# Initialize the database (make sure your MongoDB is running)
async def init():
    await init_db()

async def main():
    await init()

    # 1. Create a new conversation
    conversation_data = ConversationCreate(
        messages=[
            {"role": "user", "content": "Hello, how can I help you today?"},
            {"role": "user", "content": "My email is test@example.com"}
        ],
        user_id="user123"
    )

    new_conversation = await create_conversation(conversation_data)
    print("Created Conversation:", new_conversation)

    # 2. Read the created conversation
    conversation_id = str(new_conversation.id)
    fetched_conversation = await read_conversation(conversation_id)
    print("Fetched Conversation:", fetched_conversation)

    # 3. Update the conversation
    update_data = ConversationUpdate(
        user_id="user456",
        messages=[
            {"role": "user", "content": "This conversation has been updated."}
        ]
    )
    updated_conversation = await update_conversation(conversation_id, update_data)
    print("Updated Conversation:", updated_conversation)

    # 4. Delete the conversation
    delete_result = await delete_conversation(conversation_id)
    print("Delete Result:", delete_result)

    # Attempt to read the deleted conversation (should raise an exception)
    try:
        await read_conversation(conversation_id)
    except Exception as e:
        print(f"Error (expected since conversation was deleted): {e}")

if __name__ == "__main__":
    asyncio.run(main())
