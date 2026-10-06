import requests
import json

def solve(inputs):
    """
    Submit a new photo to JSONPlaceholder using the provided title and URL.
    
    Args:
        inputs (dict): Must contain 'new_title' and 'new_url'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        Exception: If HTTP response is unsuccessful (status code >= 400).
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Validate inputs
    if 'new_title' not in inputs or 'new_url' not in inputs:
        raise ValueError("inputs must contain 'new_title' and 'new_url'")
    
    title = inputs['new_title']
    url = inputs['new_url']
    
    endpoint = "/photos"
    full_url = f"{base_url}{endpoint}"
    
    payload = {
        "title": title,
        "url": url
    }
    
    response = requests.post(full_url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json()