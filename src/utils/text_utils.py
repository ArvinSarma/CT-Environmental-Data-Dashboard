import re
import unicodedata
import pandas as pd

def standardize_town_name(name: str) -> str:
    """
    Standardizes Connecticut town names into a consistent ASCII Title Case format.
    Handles NaN/None inputs, strips leading/trailing whitespaces, normalizes 
    unicode characters, and collapses multiple internal spaces.
    """
    if pd.isna(name) or name is None:
        return ""
    
    # Cast to string in case integers/floats are passed
    name_str = str(name)
    
    # Normalize unicode characters to standard ASCII equivalents
    normalized = unicodedata.normalize('NFKD', name_str).encode('ASCII', 'ignore').decode('utf-8')
    
    # Strip whitespace and collapse extra internal spaces
    cleaned = re.sub(r'\s+', ' ', normalized).strip()
    
    # Return normalized Title Case (e.g., "NEW CANAAN" or "new canaan" -> "New Canaan")
    return cleaned.title()