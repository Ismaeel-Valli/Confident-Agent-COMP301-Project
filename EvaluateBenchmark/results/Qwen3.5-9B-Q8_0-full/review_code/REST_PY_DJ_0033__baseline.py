import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided inputs.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and other required fields.
        
    Returns:
        int or None: The ID of the created user, or None if response is empty.
        
    Raises:
        requests.exceptions.RequestException: If HTTP request fails.
    """
    # DummyJSON API endpoint for creating a user
    url = "https://dummyjson.com/users/add"
    
    try:
        response = requests.post(url, json=inputs)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Check if the response contains an 'id' field
        if 'id' in data and data['id'] is not None:
            return data['id']
        elif data == {}:
            # Return None for successful empty response
            return None
        else:
            # If id is present but None, or other unexpected structure
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to create user: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")