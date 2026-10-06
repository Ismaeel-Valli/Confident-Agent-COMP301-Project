import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'new_title' for the album title.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful and empty.
        
    Raises:
        requests.RequestException: If HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/albums"  # Note: This endpoint does not exist in JSONPlaceholder
    
    url = f"{base_url}{endpoint}"
    
    payload = {
        "title": inputs["new_title"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200 and response.status_code != 201:
        raise requests.RequestException(f"Failed to submit album: {response.status_code}")
    
    return response.json() if response.content else None