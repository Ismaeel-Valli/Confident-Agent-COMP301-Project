import requests

def solve(inputs):
    """
    Retrieve a post by identifier from DummyJSON.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the post ID.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    url = f"https://dummyjson.com/posts/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data if data else None
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")