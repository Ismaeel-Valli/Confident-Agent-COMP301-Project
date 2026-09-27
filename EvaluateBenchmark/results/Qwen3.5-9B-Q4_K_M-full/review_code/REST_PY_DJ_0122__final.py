def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip (offset).
            - sort_field (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response, or None if empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
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
    
    # Return None for successful empty response
    if not data.get("products"):
        return None
    
    return data