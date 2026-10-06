import requests

def solve(inputs):
    """
    Deletes a user by identifier from DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' (user identifier).
        
    Returns:
        str or None: The response's id value if present, otherwise None for successful deletion.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs.get('resource_id')
    
    # DummyJSON delete endpoint pattern (assuming standard structure)
    url = f"https://dummyjson.com/users/{resource_id}"
    
    try:
        response = requests.delete(url)
        
        if response.status_code not in [200, 204]:
            raise Exception(f"Failed to delete user: {response.status_code} - {response.text}")
            
        # Return id from response if present (for 200 status), otherwise None for 204
        if response.status_code == 200 and 'id' in response.json():
            return response.json()['id']
        elif response.status_code == 204:
            return None
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {str(e)}")

# Example usage (not executed):
# inputs = {'resource_id': '1'}
# result = solve(inputs)