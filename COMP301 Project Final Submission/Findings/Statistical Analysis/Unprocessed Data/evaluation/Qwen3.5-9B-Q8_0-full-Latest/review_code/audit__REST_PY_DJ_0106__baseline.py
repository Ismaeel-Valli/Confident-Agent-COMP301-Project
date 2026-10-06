import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: The decoded JSON response as a list of users, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/users"
    
    params = {
        "_limit": inputs["result_limit"],
        "_sort": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        if not data:
            return None
        
        return data
    
    except requests.RequestException as e:
        raise e