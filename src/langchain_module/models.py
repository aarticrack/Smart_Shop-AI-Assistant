from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from src.core.config import settings

def get_llm():
    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        temperature=0.2,
        google_api_key=settings.GOOGLE_API_KEY
    )

def get_embeddings():
    return HuggingFaceEmbeddings(
        model=settings.EMBEDDING_MODEL
       
    )