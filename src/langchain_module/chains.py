from langchain_core.output_parsers import StrOutputParser
from src.langchain_module.models import get_llm
from src.langchain_module.prompts import CHAT_PROMPT
from src.data_layer.vector_store import VectorStoreManager
from src.utils.metadata_parser import extract_filters
from src.utils.logger import logger

def create_ecommerce_chain():
    llm = get_llm()
    vs_manager = VectorStoreManager()
    db = vs_manager.get_vector_db()

    def build_chroma_filter(filters: dict):
        if not filters: return None
        conditions = [{k: v} for k, v in filters.items()]
        return {"$and": conditions} if len(conditions) > 1 else conditions[0]

    def retrieve_context(input_data):
        query = input_data["question"].lower()
        filters = extract_filters(query)
        chroma_filter = build_chroma_filter(filters)

        # Detected if the user is looking for the cheapest options -extra
        is_price_query = any(word in query for word in ["cheapest", "lowest price", "starting price", "budget"])

        # 1. Fetched a larger pool if looking for "cheapest" (k=20)
        search_k = 20 if is_price_query else 5
        docs = db.similarity_search(query, k=search_k, filter=chroma_filter)

        # 2. Fallback if filter was too strict
        if not docs:
            docs = db.similarity_search(query, k=search_k)

        # 3. CHEAPEST LOGIC: Sorting the retrieved docs by the 'price' metadata
        if is_price_query and docs:
            # Sorting by price ascending (lowest first)
            docs = sorted(docs, key=lambda x: x.metadata.get('price', float('inf')))
            # Keeping only the top 5 cheapest results for the AI to process
            docs = docs[:5]
        else:
            # For normal queries, just keeping the top 3-5 most relevant
            docs = docs[:3]

        return "\n\n".join([doc.page_content for doc in docs])

    chain = (
        {
            "context": retrieve_context,
            "question": lambda x: x["question"],
            "chat_history": lambda x: x.get("chat_history", [])
        }
        | CHAT_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain