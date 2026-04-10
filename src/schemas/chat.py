from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    # The current message from the user
    message: str = Field(..., example="What are the best Dell laptops under 80k?")
    
    # This allows the multi-turn history to pass from app.py to routes.py
    # We use a list of dictionaries to match the Streamlit session_state format
    chat_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    
    session_id: Optional[str] = Field(default="default_user")

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    status: str = "success"