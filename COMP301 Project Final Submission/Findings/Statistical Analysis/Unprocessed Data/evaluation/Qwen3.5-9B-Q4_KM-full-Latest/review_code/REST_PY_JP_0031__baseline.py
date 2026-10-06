import requests


def solve(inputs):
    """
    Retrieves users from JSONPlaceholder based on provided inputs (e.g., user IDs).
    
    Args:
        inputs (list of int): List of user IDs to retrieve.
        
    Returns:
        list or None: Decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Prepare the request payload
    params = {"ids": inputs}
    
    try:
        response = requests.get(f"{base_url}/users", params=params)
        
        # Raise an exception for unsuccessful HTTP responses (status code outside 200-299)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is empty, otherwise return the data
        return data if data else None
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve users: {e}") from e