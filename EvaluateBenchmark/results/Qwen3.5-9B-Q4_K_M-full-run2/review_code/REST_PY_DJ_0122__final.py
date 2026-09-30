def solve(inputs):
    """Retrieve one page of products from DummyJSON with pagination and sorting."""
    import requests
    
    base_url = "https://dummyjson.com/products"
    
    # Build query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()