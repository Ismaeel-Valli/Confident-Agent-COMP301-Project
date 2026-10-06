import requests

def solve(inputs):
    """
    Retrieve a user by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the user ID.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/users/{}".format(resource_id)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data if data else None
        else:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")