import requests

def solve(inputs):
    """
    Retrieve a photo by identifier from JSONPlaceholder and return its id.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the photo ID.
        
    Returns:
        int or None: The photo's id, or None if absent in response.
        
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
        
        if isinstance(data, dict):
            return data.get('id')
        elif isinstance(data, list):
            if len(data) > 0:
                return data[0].get('id')
            else:
                return None
        else:
            return None
            
    except requests.RequestException as e:
        raise