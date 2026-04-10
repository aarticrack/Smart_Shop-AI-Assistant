from pydantic import BaseModel, Field
from typing import Optional

class FullQueryFilters(BaseModel):
    # Core Fields (Applies to everything)
    category: Optional[str] = Field(None, description="Category (e.g., Furniture, Kitchen Appliances, Skincare, Laptops)")
    brand: Optional[str] = Field(None, description="Brand name")
    price_lte: Optional[float] = Field(None, description="Max price in INR")
    price_gte: Optional[float] = Field(None, description="Min price in INR")
    in_stock: Optional[str] = Field(None, description="Availability: 'yes' or 'no'")
    free_shipping: Optional[str] = Field(None, description="Free shipping: 'yes' or 'no'")
    rating_gte: Optional[float] = Field(None, description="Min rating (e.g., 4.0)")
    
    # Technical & Lifestyle Specs (Dynamic)
    ram: Optional[str] = Field(None, description="Memory (Laptops/Phones)")
    storage: Optional[str] = Field(None, description="Storage capacity (Laptops/Phones)")
    material: Optional[str] = Field(None, description="Build material (Furniture/Appliances)")
    power: Optional[str] = Field(None, description="Power usage e.g. '750W' (Kitchen Appliances)")
    color: Optional[str] = Field(None, description="Item color")
    warranty_years: Optional[int] = Field(None, description="Min warranty years")