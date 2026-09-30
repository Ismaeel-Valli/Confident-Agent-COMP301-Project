import requests

def solve(inputs):
    """
    Retrieve a post by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int).
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, params={"postId": resource_id})
        response.raise_for_status()
        
        if response.status_code == 200 and not response.text.strip():
            return None
        
        return response.json()
    except requests.RequestException as e:
        raise