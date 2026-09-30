import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields': str, comma-separated list of fields to return
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/products"
    
    # Parse included_fields from comma-separated string
    fields = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters to filter fields
    params = {"fields": ",".join(fields)}
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: Failed to retrieve products")
        
        data = response.json()
        
        # Return None for successful empty response
        if not data.get("products"):
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")