from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "SmartShop Enterprise AI"
    VERSION: str = "1.0.0"
    
    # AI Infrastructure
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-3.1-flash-lite-preview"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent  #root folder of my project
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "chroma_db")
    DATA_FILE: str = str(BASE_DIR / "data" / "ecommerce_products.csv")

    # Pydantic will look for these in your .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()