from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.langchain_module.models import get_llm
from src.schemas.metadata_schema import FullQueryFilters

def extract_filters_with_llm(query: str) -> dict:
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=FullQueryFilters)

    prompt = ChatPromptTemplate.from_template(
        "You are an expert shopping assistant. Extract structured filters from the user query.\n"
        "{format_instructions}\n"
        "User Query: {query}\n"
        "Instructions: Extract category, brand, price limits, and technical specs (RAM, Power, Material, Color, etc.).\n"
        "Return ONLY the JSON object."
    )

    chain = prompt | llm | parser
    
    try:
        raw = chain.invoke({"query": query, "format_instructions": parser.get_format_instructions()})
        
        conditions = []
        # Mapping logic for ChromaDB
        for key, value in raw.items():
            if value is None: continue
            
            if key == "price_lte": conditions.append({"price": {"$lte": value}})
            elif key == "price_gte": conditions.append({"price": {"$gte": value}})
            elif key == "rating_gte": conditions.append({"rating": {"$gte": value}})
            elif key == "warranty_years": conditions.append({"warranty_years": {"$gte": value}})
            else:
                # String fields: brand, category, ram, storage, material, power, color, in_stock, etc.
                conditions.append({key: str(value).lower().strip()})
        
        if len(conditions) > 1:
            return {"$and": conditions}
        return conditions[0] if conditions else {}
        
    except Exception:
        return {}