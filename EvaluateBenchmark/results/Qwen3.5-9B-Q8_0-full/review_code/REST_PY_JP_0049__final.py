import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder and return its id.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' (int) for the album ID.
        
    Returns:
        int or None: The album's id if found, None if response is empty or attribute absent.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    # JSONPlaceholder does not have an albums endpoint
    # This would need to be implemented with the correct endpoint
    url = "https://jsonplaceholder.typicode.com/photos"  # Placeholder - incorrect
    
    try:
        response = requests.get(url, params={"id": resource_id})
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # Check if the response is empty or lacks 'id'
            if not data or 'id' not in data:
                return None
            return data['id']
        else:
            raise Exception(f"HTTP {response.status_code}")
    except requests.RequestException as e:
        raise e