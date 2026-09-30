import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: Decoded JSON response as a list of users, or None if empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/users"
    params = {
        "limit": inputs["result_limit"],
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
    
    data = response.json()
    users = data.get("users", [])
    
    return users if users else None