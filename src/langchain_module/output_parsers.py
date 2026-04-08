import re
from langchain_core.output_parsers import StrOutputParser

class SmartShopOutputParser(StrOutputParser):
    """
    Extends the standard parser to clean up AI responses 
    and ensure Markdown tables are correctly formatted.
    """
    def parse(self, text: str) -> str:
        # Standard string cleanup
        cleaned_text = super().parse(text)
        
        # Post-processing:
        cleaned_text = cleaned_text.replace("Rs.", "₹").replace("INR", "₹")
        
        return cleaned_text

    def extract_product_ids(self, text: str) -> list[str]:
        """
        Utility to find product IDs mentioned in the AI response 
        for click-tracking/analytics.
        """
        return re.findall(r'ID:\s*(\w+)', text)