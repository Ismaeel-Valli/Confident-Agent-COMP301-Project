import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on provided sorting parameters.
    
    Args:
        inputs (dict): A dictionary containing:
            - sort_field (str): Field used for ordering.
            - sort_direction (str): Ordering direction ('asc' or 'desc').
    
    Returns:
        list or None: The decoded JSON response as a list of products, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    base_url = "https://dummyjson.com/products"
    params = {
        "sort": inputs["sort_field"],
        "order": inputs["sort_direction"],
        "skip": 0,
        "limit": 1
    }

    response = requests.get(base_url, params=params)
    
    if not response.ok:
        raise requests.exceptions.HTTPError(f"HTTP {response.status_code}: {response.text}")

    data = response.json()
    
    if not data.get("products"):
        return None
    
    return data["products"]