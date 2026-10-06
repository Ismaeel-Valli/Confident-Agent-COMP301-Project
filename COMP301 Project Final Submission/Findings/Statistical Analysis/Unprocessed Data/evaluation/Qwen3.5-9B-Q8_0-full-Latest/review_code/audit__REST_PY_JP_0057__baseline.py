import requests

def solve(inputs):
    """
    Retrieves todos from JSONPlaceholder filtered by user_id.
    
    Args:
        inputs (dict): A dictionary containing 'user_identifier' key.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if the list is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    user_id = inputs.get('user_identifier')
    
    if user_id is None:
        raise ValueError("Missing required 'user_identifier' in inputs.")

    url = "https://jsonplaceholder.typicode.com/todos"
    params = {'userId': user_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    if not data:
        return None
        
    return data