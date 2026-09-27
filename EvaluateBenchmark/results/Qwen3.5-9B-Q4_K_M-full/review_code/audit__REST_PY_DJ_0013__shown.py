import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON and return the decoded JSON response.
    
    Args:
        inputs (dict): Must contain 'post_id' key with an integer value representing the post ID.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for a successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    endpoint = f"/posts/{inputs['post_id']}"
    url = base_url + endpoint
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data if data else None
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {e}")