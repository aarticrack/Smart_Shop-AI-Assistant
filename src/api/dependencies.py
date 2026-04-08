from src.data_layer.repository import ProductRepository
from src.langchain_module.chains import create_ecommerce_chain

def get_repository() -> ProductRepository:
    return ProductRepository()

def get_chat_chain():
    return create_ecommerce_chain()