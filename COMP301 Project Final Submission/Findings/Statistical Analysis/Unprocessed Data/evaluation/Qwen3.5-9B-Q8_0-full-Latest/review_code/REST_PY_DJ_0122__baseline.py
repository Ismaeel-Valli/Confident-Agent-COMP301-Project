import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on skip count and sort field.
    
    Args:
        inputs (dict): A dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - sort_field (str): Field used for ordering.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "sort": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a list under the 'products' key or directly as a list depending on version/endpoint structure.
    # Standard GET /products returns {'products': [...], 'total': ..., 'skip': ..., 'limit': ...}
    if "products" in data:
        products = data["products"]
    else:
        products = data
    
    return None if not products else products