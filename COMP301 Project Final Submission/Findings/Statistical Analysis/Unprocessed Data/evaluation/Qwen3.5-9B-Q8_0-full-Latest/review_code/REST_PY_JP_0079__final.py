import requests

def solve(inputs):
    """
    Retrieve a photo by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the photo ID.
        
    Returns:
        str or None: The title of the photo, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for unsuccessful responses
        
        data = response.json()
        
        if not data:
            return None
            
        title = data.get('title')
        return title if title is not None else None
        
    except requests.RequestException as e:
        raise