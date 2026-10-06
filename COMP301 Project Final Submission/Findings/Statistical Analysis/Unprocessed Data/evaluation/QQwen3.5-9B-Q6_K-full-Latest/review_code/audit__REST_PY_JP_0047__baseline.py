import requests

def solve(inputs):
    """
    Retrieves albums from JSONPlaceholder filtered by userId.
    
    Args:
        inputs (dict): A dictionary containing 'user_identifier' key.
        
    Returns:
        list or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    user_id = inputs.get('user_identifier')
    
    if not user_id:
        raise ValueError("Missing 'user_identifier' in inputs")

    url = "https://jsonplaceholder.typicode.com/albums"
    params = {'userId': user_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    return data if data else None