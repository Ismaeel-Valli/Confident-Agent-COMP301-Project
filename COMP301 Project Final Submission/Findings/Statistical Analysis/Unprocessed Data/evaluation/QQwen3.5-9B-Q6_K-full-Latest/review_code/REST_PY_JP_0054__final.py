import requests

def solve(inputs):
    """
    Retrieve a photo by identifier from JSONPlaceholder and return its id.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the photo ID.
        
    Returns:
        int or None: The photo's id if found, None for empty response or missing attribute.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
            
        if 'id' in data:
            return data['id']
            
        return None
        
    except requests.exceptions.RequestException as e:
        raise e