import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the album title.
        
    Returns:
        str or None: The title of the created album, or None if the response is empty/successful without data.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/albums"
    
    payload = {
        "title": inputs.get("new_title")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to create album. Status code: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
        
    return data.get("title")