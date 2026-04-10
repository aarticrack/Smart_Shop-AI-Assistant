from fastapi import APIRouter
from src.schemas.chat import ChatRequest
from src.langchain_module.chains import create_ecommerce_chain
from langchain_core.messages import HumanMessage, AIMessage
from src.utils.logger import logger

router = APIRouter()

# Initializing the chain once at startup
ecommerce_chain = create_ecommerce_chain()

# In-memory session store (Dictionary-based history)
# Key: session_id, Value: List of Human/AI Message objects
sessions_db = {}

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message
    
    # 1. Retrieving or initializing history for this specific user
    if session_id not in sessions_db:
        sessions_db[session_id] = []
    
    chat_history = sessions_db[session_id]
    
    logger.info(f"Session {session_id} - User: {user_message}")

    try:
        # 2. Invoke the chain with history
        # This triggers the 'standalone_question' logic we built in chains.py
        response_text = ecommerce_chain.invoke({
            "question": user_message,
            "chat_history": chat_history
        })

        # 3. Updated the history buffer for the next turn
        chat_history.append(HumanMessage(content=user_message))
        chat_history.append(AIMessage(content=response_text))
        
        # Keep history manageable (last 10 messages) to prevent context bloat
        if len(chat_history) > 10:
            sessions_db[session_id] = chat_history[-10:]

        return {"answer": response_text}

    except Exception as e:
        logger.error(f"Chat Error: {str(e)}")
        return {"answer": "I'm having trouble processing that request. Please try again."}