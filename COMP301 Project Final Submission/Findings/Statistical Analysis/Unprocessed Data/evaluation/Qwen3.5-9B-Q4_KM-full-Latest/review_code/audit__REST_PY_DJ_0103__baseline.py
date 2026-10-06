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
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/products"
    
    # Construct query parameters
    params = {
        "_limit": inputs["result_limit"],
        "_sort": inputs["sort_field"]
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty
        if not data:
            return None
            
        return data
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve products: {e}") from e