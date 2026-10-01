import requests

def solve(inputs):
    """
    Retrieve posts from JSONPlaceholder and return the decoded JSON response.
    
    Parameters:
        inputs (dict): Must contain 'post_id' key with an integer value.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200 and len(response.json()) == 0:
            return None
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")