import requests

def solve(inputs):
    """
    Retrieves a user by identifier from DummyJSON API and returns the user's ID.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the user identifier.
        
    Returns:
        int or None: The user's ID if found, None for successful empty response or missing ID attribute.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs.get('resource_id')
    url = f"https://dummyjson.com/users/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Check if the response is empty (no users found or similar)
        if not data.get('users'):
            return None
            
        # Return the id of the first user in the list, or None if absent
        user_list = data.get('users', [])
        if user_list:
            user_id = user_list[0].get('id')
            return user_id if user_id is not None else None
            
    except requests.exceptions.RequestException as e:
        raise e

# Example usage (not executed):
# inputs = {'resource_id': 1}
# result = solve(inputs)