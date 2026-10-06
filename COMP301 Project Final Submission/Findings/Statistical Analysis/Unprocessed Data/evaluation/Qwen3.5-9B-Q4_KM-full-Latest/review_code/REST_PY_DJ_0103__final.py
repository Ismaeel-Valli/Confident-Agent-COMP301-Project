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
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()