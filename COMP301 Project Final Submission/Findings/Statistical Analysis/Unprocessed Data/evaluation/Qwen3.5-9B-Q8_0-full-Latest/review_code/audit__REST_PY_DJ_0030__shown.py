import requests

def solve(inputs):
    """
    Retrieve a user by identifier from DummyJSON and return the user's id.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the user identifier.
        
    Returns:
        int or None: The user's id, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        raise ValueError("Missing required 'resource_id' in inputs")
    
    url = f"https://dummyjson.com/users/{resource_id}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises exception for unsuccessful HTTP responses
    
    data = response.json()
    
    # Return the id if present, otherwise None
    return data.get('id')