import requests

def solve(inputs):
    """
    Retrieve a todo by identifier from JSONPlaceholder and return its id.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the todo ID to fetch.
        
    Returns:
        int or None: The todo's id if found, None for empty response or missing attribute.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/todos"
    
    try:
        response = requests.get(url, params={'id': resource_id})
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        data = response.json()
        
        # Handle empty response
        if not data:
            return None
        
        # Check if 'id' attribute exists in the response
        if isinstance(data, dict) and 'id' in data:
            return data['id']
        elif isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
            return data[0]['id']
        
        # If we get here, id is missing from the response structure
        return None
            
    except requests.RequestException as e:
        raise