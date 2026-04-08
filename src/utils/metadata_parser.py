import re
def extract_filters(query: str):
    query = query.lower()
    filters = {}

    # Category Mapping
    category_map = {
        "laptop": "Laptops",
        "phone": "Smartphones",
        "headphone": "Headphones",
        "camera": "Cameras"
    }
    for key, value in category_map.items():
        if key in query:
            filters["category"] = value

    # Updated Brand Mapping (Case Insensitive for Search, Capitalized for Filter)
    brands = ['hp', 'dell', 'lenovo', 'apple', 'asus', 'acer', 'samsung', 'sony', 'vivo', 'oneplus', 'xiaomi', 'realme']
    for brand in brands:
        if brand in query:
            # We capitalize it here because  CSV values are likely 'Samsung', 'Apple', etc.
            filters['brand'] = brand.capitalize() if brand != 'hp' else 'HP'

    # Price Extraction
    price_match = re.search(r"(under|below|less than)\s?(\d+)", query)
    if price_match:
        filters['price'] = {'$lte': float(price_match.group(2))}

    return filters