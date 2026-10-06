import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: The decoded JSON response as a list of products, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "limit": inputs.get("result_limit", 10),
        "sort": inputs.get("sort_field", "")
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a structure like {"products": [...], "total": ..., ...}
    products = data.get("products", [])
    
    if not products:
        return None
    
    return products