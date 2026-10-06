import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, skipping results_to_skip items,
    sorted by sort_field. Returns decoded JSON response or None for empty response.
    Raises exception on unsuccessful HTTP response.
    """
    base_url = "https://dummyjson.com/products"
    
    # Construct the query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response (products array is empty)
    if not data.get("products"):
        return None
    
    return data