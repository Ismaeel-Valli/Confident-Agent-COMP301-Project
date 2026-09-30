import requests

def solve(inputs):
    """
    Retrieve a user by identifier from JSONPlaceholder and return their name.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the user ID to retrieve.
        
    Returns:
        str or None: The user's name if found, None for empty response or missing name.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        raise ValueError("Missing required parameter: resource_id")
    
    url = "https://jsonplaceholder.typicode.com/users"
    params = {'id': resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
        
        data = response.json()
        
        # Handle empty response
        if not data:
            return None
        
        # Return name if present, otherwise None
        return data.get('name')
    
    except requests.exceptions.HTTPError as e:
        raise e  # Re-raise HTTP errors as required
    except requests.exceptions.RequestException as e:
        raise e  # Re-raise other request exceptions