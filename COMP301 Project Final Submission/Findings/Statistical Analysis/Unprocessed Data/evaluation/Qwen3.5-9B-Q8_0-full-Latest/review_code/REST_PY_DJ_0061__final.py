import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with specified fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/products"
    
    # Parse included_fields from comma-separated string
    fields = inputs["included_fields"].split(",") if inputs["included_fields"] else []
    
    # Build query parameters for field selection
    params = {"include": ",".join(fields)} if fields else {}
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response (empty products array)
        if not data.get("products"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")