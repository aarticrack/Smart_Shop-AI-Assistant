import pandas as pd
import json
from langchain_core.documents import Document
from src.core.config import settings
from src.data_layer.vector_store import VectorStoreManager
from langchain_community.vectorstores import Chroma
from src.utils.logger import logger

def parse_specs(specs_text):
    """Parses the JSON string found in the CSV specs column."""
    specs = {}
    if not isinstance(specs_text, str) or not specs_text.strip():
        return specs
    try:
        # Loading  JSON format: {"RAM": "64GB", "Storage": "256GB SSD", ...}
        data = json.loads(specs_text)
        for key, value in data.items():
            # Cleaning keys and values: 'RAM' -> 'ram', '64GB' -> '64gb'
            clean_key = key.strip().lower()
            clean_val = str(value).strip().lower().replace(" ", "")
            specs[clean_key] = clean_val
    except json.JSONDecodeError:
        logger.warning(f"Skipping invalid JSON specs: {specs_text}")
    return specs

def run_ingestion():
    logger.info(f" Starting Data Ingestion from {settings.DATA_FILE}")
    try:
        df = pd.read_csv(settings.DATA_FILE)
        df.columns = df.columns.str.strip() 
        
        documents = []
        #for _, row in df.iterrows():
            # Searchable text for semantic context
            #searchable_text = " ".join([f"{col}: {val}" for col, val in row.items()])

        for _, row in df.iterrows():
            # Creating a structured text block for the LLM to read easily
            searchable_text = f"""
            Product: {row.get('name')}
            Brand: {row.get('brand')}
            Category: {row.get('category')}
            Price: INR {row.get('price_inr')}
            Rating: {row.get('rating')} stars
            Description: {row.get('description')}
            Specs: {row.get('specs')}
            Warranty: {row.get('warranty_years')} years
            Shipping: {'Free' if str(row.get('free_shipping')).lower() == 'yes' else 'Standard'}
            """
            
    
            
            # Metadata for 'Hard' filtering logic
            specs_data = parse_specs(row.get('specs', "{}"))
            metadata = {
                "product_id": int(row.get('product_id', 0)),
                "name": str(row.get('name', "")).lower(),
                "brand": str(row.get('brand', '')).lower().strip(),
                "price": float(row.get('price_inr', 0)),
                "stock_status": str(row.get('in_stock', 'no')).lower().strip(),
                "category": str(row.get('category', "")).lower().strip(),
                "rating": float(row.get('rating', 0)),
                "warranty_years": int(row.get("warranty_years", 0)),
                "return_days": int(row.get("return_policy_days", 0)),
                "free_shipping": str(row.get("free_shipping", "no")).lower().strip(),
                **specs_data # This automatically adds 'ram', 'storage', etc.
            }
            
            documents.append(Document(page_content=searchable_text, metadata=metadata))

        manager = VectorStoreManager()
        logger.info(f" Saving {len(documents)} docs to {settings.CHROMA_PERSIST_DIR}")
        
        # Fresh initialization
        Chroma.from_documents(
            documents=documents,
            embedding=manager.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )
        logger.info("SUCCESS: Ingestion Complete!")
        
    except Exception as e:
        logger.error(f"❌ Ingestion Failed: {str(e)}")

if __name__ == "__main__":
    run_ingestion()