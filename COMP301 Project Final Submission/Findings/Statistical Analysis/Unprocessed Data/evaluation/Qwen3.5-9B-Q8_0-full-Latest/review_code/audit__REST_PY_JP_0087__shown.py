import requests

def solve(inputs):
    """
    Retrieve a user by identifier from JSONPlaceholder and return their name.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the user ID to retrieve.
        
    Returns:
        str or None: The user's name if found, None for empty response.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    
    # JSONPlaceholder users endpoint: GET /users/{id}
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
        
        data = response.json()
        
        # Check if response is empty or doesn't have 'name' attribute
        if not data or 'name' not in data:
            return None
            
        return data['name']
        
    except requests.RequestException as e:
        raise e