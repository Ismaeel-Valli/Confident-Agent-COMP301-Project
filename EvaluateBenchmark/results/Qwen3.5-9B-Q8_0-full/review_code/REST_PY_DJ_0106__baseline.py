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
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/users"
    
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'users' key. We return the list of users.
    users = data.get("users", [])
    
    if not users:
        return None
    
    return users