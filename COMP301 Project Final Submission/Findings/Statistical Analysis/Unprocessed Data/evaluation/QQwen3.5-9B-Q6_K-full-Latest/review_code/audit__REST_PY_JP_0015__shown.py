import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the album ID.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/photos"
    
    try:
        response = requests.get(url, params={"albumId": resource_id})
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return None if len(data) == 0 else data
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")