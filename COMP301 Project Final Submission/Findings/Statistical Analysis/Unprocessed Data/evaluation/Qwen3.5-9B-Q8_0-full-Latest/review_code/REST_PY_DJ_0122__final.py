import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Must contain 'results_to_skip' (int) and 'sort_field' (str).
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty products array)
    if not data.get("products"):
        return None
    
    return data