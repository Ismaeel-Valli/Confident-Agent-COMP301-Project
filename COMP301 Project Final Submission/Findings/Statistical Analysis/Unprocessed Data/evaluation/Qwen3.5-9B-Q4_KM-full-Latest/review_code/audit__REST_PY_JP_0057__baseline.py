import requests

def solve(inputs):
    """
    Retrieves todos from JSONPlaceholder filtered by userId.
    
    Args:
        inputs (dict): A dictionary containing 'user_identifier' (userId).
        
    Returns:
        list or None: The decoded JSON response as a list of todos, or None if the response is empty.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    user_id = inputs['user_identifier']
    url = f"https://jsonplaceholder.typicode.com/todos?userId={user_id}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    todos = response.json()
    
    return None if not todos else todos