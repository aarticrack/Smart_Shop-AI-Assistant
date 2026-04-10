import pandas as pd
import json
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from src.core.config import settings
from src.data_layer.vector_store import VectorStoreManager
from src.utils.logger import logger

def parse_specs(specs_text):
    """
    Parses the JSON string found in the CSV specs column.
    Handles all categories by cleaning keys and values for better filtering.
    """
    specs = {}
    if not isinstance(specs_text, str) or not specs_text.strip():
        return specs
    try:
        # Loading JSON format (e.g., {"Power": "750W", "Material": "Wood", "RAM": "16GB"})
        data = json.loads(specs_text)
        for key, value in data.items():
            # Cleaned keys: 'Power' -> 'power', 'Material' -> 'material'
            # Cleaned values: '750W' -> '750w'
            clean_key = key.strip().lower()
            clean_val = str(value).strip().lower()
            specs[clean_key] = clean_val
    except json.JSONDecodeError:
        logger.warning(f"Skipping invalid JSON specs: {specs_text}")
    return specs

def run_ingestion():
    """
    Main pipeline to load CSV, process all columns + JSON specs, 
    and index them into ChromaDB.
    """
    logger.info(f"Starting Data Ingestion from {settings.DATA_FILE}")
    
    try:
        # Loaded the dataset
        df = pd.read_csv(settings.DATA_FILE)
        df.columns = df.columns.str.strip() 
        
        documents = []

        for _, row in df.iterrows():
            # 1. Creating a rich searchable text block for Semantic Search
            # This allows the LLM to 'read' the product naturally.
            searchable_text = f"""
            Product: {row.get('name')}
            Brand: {row.get('brand')}
            Category: {row.get('category')}
            Price: INR {row.get('price_inr')}
            Rating: {row.get('rating')} stars
            Description: {row.get('description')}
            Tags: {row.get('tags')}
            Specs: {row.get('specs')}
            free_shipping:{row.get('free_shipping')}
            warranty_years:{row.get('warranty_years')}
            return_days:{row.get('return_policy_days')}
            

            """
            
            # 2. Extracting and flattening JSON specs (e.g., Power, Material, RAM)
            specs_data = parse_specs(row.get('specs', "{}"))
            
            # 3. Building comprehensive Metadata for Hard Filtering
            # Includes all standard columns + flattened dynamic specs
            metadata = {
                "product_id": int(row.get('product_id', 0)),
                "name": str(row.get('name', "")).lower(),
                "brand": str(row.get('brand', '')).lower().strip(),
                "category": str(row.get('category', "")).lower().strip(),
                "price": float(row.get('price_inr', 0)),
                "rating": float(row.get('rating', 0)),
                "in_stock": str(row.get('in_stock', 'no')).lower().strip(),
                "free_shipping": str(row.get("free_shipping", "no")).lower().strip(),
                "warranty_years": int(row.get("warranty_years", 0)),
                "return_days": int(row.get("return_policy_days", 0)),
                **specs_data # This adds keys like 'material', 'power', 'ram', etc.
            }
            
            documents.append(Document(page_content=searchable_text, metadata=metadata))

        # 4. Saving to Vector Store
        manager = VectorStoreManager()
        logger.info(f" Saving {len(documents)} products to {settings.CHROMA_PERSIST_DIR}")
        
        # Fresh initialization using Chroma
        Chroma.from_documents(
            documents=documents,
            embedding=manager.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )
        
        logger.info(" SUCCESS: Full Catalog Ingestion Complete!")
        
    except Exception as e:
        logger.error(f" Ingestion Failed: {str(e)}")

if __name__ == "__main__":
    run_ingestion()