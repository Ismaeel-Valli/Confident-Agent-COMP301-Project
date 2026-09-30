import requests

def solve(inputs):
    """
    Deletes a user by identifier from DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the user identifier.
        
    Returns:
        bool or None: The 'isDeleted' value from the response, or None if absent or on success with empty response.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response is unsuccessful (status code 4xx or 5xx).
    """
    resource_id = inputs.get('resource_id')
    
    # Base URL for DummyJSON API
    base_url = "https://dummyjson.com"
    endpoint = f"/user/{resource_id}"
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.delete(url)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response is empty (successful deletion often returns empty body)
        if not response.text.strip():
            return None
            
        # Parse the JSON response
        data = response.json()
        
        # Return the 'isDeleted' value if present, otherwise None
        return data.get('isDeleted')
        
    except requests.exceptions.HTTPError as e:
        raise e