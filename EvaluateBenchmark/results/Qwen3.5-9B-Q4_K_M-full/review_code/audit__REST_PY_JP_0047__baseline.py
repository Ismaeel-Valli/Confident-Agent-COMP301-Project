import requests

def solve(inputs):
    """
    Retrieves albums from JSONPlaceholder filtered by userId.
    
    Args:
        inputs (dict): A dictionary containing 'user_identifier' to filter by userId.
        
    Returns:
        list or None: The decoded JSON response as a list of albums, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    user_id = inputs.get('user_identifier')
    
    # Construct the URL with the userId query parameter
    url = f"https://jsonplaceholder.typicode.com/albums?userId={user_id}"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is empty (though unlikely for this endpoint with a valid userId)
        return data if data else None
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve albums: {e}") from e