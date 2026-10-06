import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key with a string value.
        
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    sort_field = inputs["sort_field"]
    
    url = f"{base_url}?sort=-{sort_field}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("products"):
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")