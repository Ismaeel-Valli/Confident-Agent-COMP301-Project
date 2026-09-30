import requests

def solve(inputs):
    """
    Retrieve a user by identifier from JSONPlaceholder and return only the id value.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the user identifier.
        
    Returns:
        int or None: The user's id if present, None for empty response or missing attribute.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    url = "https://jsonplaceholder.typicode.com/users"
    params = {'id': resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises exception for unsuccessful HTTP responses
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle empty response
            if not data:
                return None
            
            # Check if 'id' attribute is present
            if 'id' in data:
                return data['id']
            else:
                return None
                
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {e}")