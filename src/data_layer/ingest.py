import pandas as pd
from langchain_core.documents import Document
from src.core.config import settings
from src.data_layer.vector_store import VectorStoreManager
from langchain_community.vectorstores import Chroma
from src.utils.logger import logger  # Ensuring the project logger is used


def parse_specs(specs_text):
    specs={}
    if not isinstance(specs_text,str):
        return specs
    parts=specs_text.split(" ,")
    for part in parts:
        if ":" in part:
            key, value=part.split(":",1)
            specs[key.strip().lower()]=value.strip().lower()
    return specs

def run_ingestion():
    logger.info(f" Starting Data Ingestion from {settings.DATA_FILE}")
    
    try:
        # Load CSV and clean up column names (handles 'name' vs 'product_name')
        df = pd.read_csv(settings.DATA_FILE)
        df.columns = df.columns.str.strip() 
        
        logger.info(f" Found {len(df)} products with columns: {list(df.columns)}")
        
        documents = []
        for _, row in df.iterrows():
            # COMBINE EVERY COLUMN: This ensures Name, Price, and Description are all searchable
            searchable_text = " ".join([f"{col}: {val}" for col, val in row.items()])
            
            # MAP METADATA: Used for the 'stock_status' filter in vector_store.py

            specs_data=parse_specs(row.get('specs',""))
            metadata = {

                
            
                "product_id":int(row.get('product_id', 0)),
                "name":str(row.get('name',"")).lower(),                   #export PYTHONPATH=$PYTHONPATH:.python3 src/data_layer/ingest.py

                "brand":str(row.get('brand', ' ')).lower(),
                "price": float(row.get('price_inr', 0)),
                "stock_status": str(row.get('in_stock', 'no')).lower().strip(),
                "category":str(row.get('category',"")).lower(),
                
                "rating": float(row.get('rating', 0)),
               
                "warranty_years":int(row.get("warranty_years",0)),
               
                "return_days":int(row.get("return_policy_days",0)),
                "free_shipping":str(row.get("free_shipping","no")).lower().strip(),
                **specs_data
            }
            
            documents.append(Document(page_content=searchable_text, metadata=metadata))

        # Initializing Vector Store
        manager = VectorStoreManager()
        logger.info(f"Saving {len(documents)} documents to ChromaDB at {settings.CHROMA_PERSIST_DIR}")
        
        db = Chroma.from_documents(
            documents=documents,
            embedding=manager.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )
        
        logger.info("SUCCESS: Ingestion Complete. All columns are now indexed!")
        
    except Exception as e:
        logger.error(f"ERROR during ingestion: {str(e)}")

if __name__ == "__main__":
    run_ingestion()