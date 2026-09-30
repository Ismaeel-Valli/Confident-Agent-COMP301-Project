import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Contains 'results_to_skip' (int) and 'sort_field' (str).
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data.get("products"):
        return None
    
    return data