from typing import List, Optional
from src.data_layer.vector_store import VectorStoreManager
from langchain_core.documents import Document

class ProductRepository:
    def __init__(self):
        self.manager = VectorStoreManager()
        self.retriever = self.manager.get_retriever()

    def find_similar_products(self, query: str, limit: int = 5) -> List[Document]:
        """
        Fetches products matching the semantic intent of the user.
        """
        # We use the retriever configured in vector_store.py (which handles stock filters)
        return self.retriever.get_relevant_documents(query)

    def get_product_by_id(self, product_id: str) -> Optional[Document]:
        """
        Direct lookup for a specific product ID.
        """
        db = self.manager.get_vector_db()
        results = db.get(where={"id": product_id})
        if results["documents"]:
            return results["documents"][0]
        return None