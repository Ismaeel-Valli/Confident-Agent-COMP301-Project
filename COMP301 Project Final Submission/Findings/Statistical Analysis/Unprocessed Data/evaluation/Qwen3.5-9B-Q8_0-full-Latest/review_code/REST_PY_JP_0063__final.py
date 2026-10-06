import requests

def solve(inputs):
    """
    Retrieve a user by identifier from JSONPlaceholder and return the user's id.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the user ID.
        
    Returns:
        int or None: The user's id if found, None if response is empty or attribute absent.
        
    Raises:
        requests.RequestException: If HTTP request fails.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/users"
    params = {'id': resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
            
        if 'id' in data:
            return data['id']
            
        return None
        
    except requests.RequestException as e:
        raise