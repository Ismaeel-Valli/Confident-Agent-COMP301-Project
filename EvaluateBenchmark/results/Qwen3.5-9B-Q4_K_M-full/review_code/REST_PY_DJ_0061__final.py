import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON using the provided fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields': str, comma-separated list of fields to return
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    included_fields = inputs["included_fields"]
    
    url = f"{base_url}?include={included_fields}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("products"):
            return None
        
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")