import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "limit": inputs["result_limit"],
        "sort_by": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        products = data.get("products", [])
        
        return products if products else None
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")