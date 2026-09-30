import requests

def solve(inputs):
    """
    Updates selected fields of a post on DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_user_identifier' (new user ID).
        
    Returns:
        str or None: The response's id value if present, otherwise None for successful empty response.
        Raises: Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    new_user_identifier = inputs.get('new_user_identifier')
    
    # Base URL for DummyJSON API
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts/{resource_id}"
    
    payload = {
        "userId": new_user_identifier
    }
    
    try:
        response = requests.put(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx and 5xx)
        response.raise_for_status()
        
        # Check if the response is empty (204 No Content or similar)
        if response.status_code == 204:
            return None
        
        # Try to get the id from the response JSON
        try:
            data = response.json()
            return data.get('id')
        except ValueError:
            # If response is not valid JSON but status is OK, return None
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")