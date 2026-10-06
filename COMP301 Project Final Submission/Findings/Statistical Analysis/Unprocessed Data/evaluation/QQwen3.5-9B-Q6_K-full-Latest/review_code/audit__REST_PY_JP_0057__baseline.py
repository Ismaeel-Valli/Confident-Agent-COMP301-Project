import requests

def solve(inputs):
    """
    Retrieves todos from JSONPlaceholder filtered by user_id.
    
    Args:
        inputs (dict): Must contain 'user_identifier' key with an integer value.
        
    Returns:
        list or None: Decoded JSON response if successful, None for empty list.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    user_id = inputs.get('user_identifier')
    
    if user_id is None:
        raise ValueError("Missing 'user_identifier' in inputs")

    url = "https://jsonplaceholder.typicode.com/todos"
    params = {'userId': user_id}
    
    response = requests.get(url, params=params)
    
    if not response.ok:
        raise requests.exceptions.RequestException(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    return data if data else None