from langchain_chroma import Chroma
from src.langchain_module.models import get_embeddings
from src.core.config import settings
from src.utils.logger import logger

class VectorStoreManager:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.persist_dir = settings.CHROMA_PERSIST_DIR

    def get_vector_db(self):
        try:
            return Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings
            )
        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            raise

    

        